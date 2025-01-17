from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm, PostForm
from .models import Post, Category, Comment


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"

    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(title__icontains=query)
        return Post.objects.all()

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        # print(kwargs)
        context = super().get_context_data(**kwargs)
        # print(context)
        context['comments'] = Comment.objects.filter(post=context['post'])

        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'

    def get_queryset(self):
        return Category.objects.filter(name=self.kwargs['category_name'])

    def get_context_data(self, **kwargs):
        # print(kwargs)
        context = super().get_context_data(**kwargs)
        print(context)
        context['posts'] = Post.objects\
            .filter(categories__name__contains=self.kwargs['category_name']).order_by("-created_on")
        context['category_name'] = self.kwargs['category_name']

        return context


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author  = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:blog_detail", args=[self.object.id])


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post

    fields = ['title', 'body', 'categories']
        
    def get_success_url(self):
        return reverse('blog:blog_detail', args = [self.object.id])
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    # def handle_no_permission(self):
    #     raise PermissionDenied("You cannot modify other people's posts.")


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post

    def get_success_url(self):

        return reverse_lazy('blog:blog_index')
    
    def test_func(self):
        post = self.get_object()

        return self.request.user == post.author



class CommentCreateView(LoginRequiredMixin,CreateView):

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['author']  = self.request.user
    #     return initial
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs["post_id"]) 
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs["post_id"])
        context['post'] = post
        return context
    
    def get_success_url(self):
        return reverse("blog:blog_detail", args=[self.object.post.id])

    
class CommentUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

    model = Comment
    fields = ["body"]

    def get_object(self, queryset=None):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        return comment

    def form_valid(self, form):
        comment = self.object
        form.instance.post = Post.objects.get(id=self.kwargs["post_id"]) 
        form.instance.author = comment.author
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs["post_id"])
        context['post'] = post
        return context

    def get_success_url(self, **kwargs):
        return reverse("blog:blog_detail", args=[self.object.post_id])

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        else:
            raise PermissionDenied("You cannot modify other users' posts.")
    

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    model = Comment

    def get_object(self, queryset=None):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        return comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs["post_id"])
        context['post'] = post
        return context

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', args=[self.object.post_id])

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        else:
            raise PermissionDenied("You cannot modify other users' posts.")


# Custom 403 handler
# def custom_403_view(request, exception=None):
#     return render(request, 'blog/403.html', status=403)