from django.urls import path
from .views import PostListView, PostDetailView, CategoryListView


urlpatterns = [
    path("", PostListView.as_view(), name="blog_index"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("category/<category_name>/", CategoryListView.as_view(), name='blog_category'),
   ]