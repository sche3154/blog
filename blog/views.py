from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import CommentForm
from .models import Post, Category, Comment

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"

    context_object_name = 'posts'

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

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'categories']

    def get_success_url(self):
        return reverse("blog:blog_detail", args=[self.object.id])


class PostUpdateView(UpdateView):
    model = Post

    fields = ['title', 'body', 'categories']
        

    def get_success_url(self):

        return reverse('blog:blog_detail', args = [self.object.id])


class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):

        return reverse('blog:blog_index')


class CommentCreateView(CreateView):

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    
    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs["post_id"]) 
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs["post_id"])
        context['post'] = post
        return context
    
    def get_success_url(self):
        return reverse("blog:blog_detail", args=[self.object.post.id])

class CommentUpdateView(UpdateView):

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
    
class CommentDeleteView(DeleteView):

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


