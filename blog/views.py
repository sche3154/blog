from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Post, Category, Comment
from django.views.generic import ListView, DetailView

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"

    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    
class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'

    def get_queryset(self) -> QuerySet[Any]:
        return Category.objects.filter(name=self.kwargs['category_name'])

    def get_context_data(self):
        context = super().get_context_data()
        context['posts'] = Post.objects\
            .filter(categories__name__contains=self.kwargs['category_name']).order_by("-created_on")
        context['category_name'] = self.kwargs['category_name']

        return context

