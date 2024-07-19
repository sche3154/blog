from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView\
, CategoryListView, CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="blog_index"),
    path("post/post_create", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("post/<int:pk>/post_update", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/post_delete", PostDeleteView.as_view(), name="post_delete"),
    path("category/<category_name>/", CategoryListView.as_view(), name='blog_category'),
    path("post/<int:post_id>/comment_create/", CommentCreateView.as_view(), name='comment_create'),
    path("post/<int:post_id>/comment_update/<int:comment_id>", CommentUpdateView.as_view(), name='comment_update'),
    path("post/<int:post_id>/comment_delete/<int:comment_id>", CommentDeleteView.as_view(), name='comment_delete')
   ]