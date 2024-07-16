from django.urls import path
from .views import PostListView, PostDetailView, CategoryListView, CommentCreateView

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="blog_index"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("category/<category_name>/", CategoryListView.as_view(), name='blog_category'),
    path("post/<int:post_id>/comment_create/", CommentCreateView.as_view(), name='comment_create')
   ]