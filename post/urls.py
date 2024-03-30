from django.urls import path
from .views import GetPosts, DeletePost, DeleteAllPosts, CreatePostView, UpatePost

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('<int:user_id>/get', GetPosts.as_view(), name='get-post'),
    path('<int:user_id>/<int:post_id>/delete', DeletePost.as_view(), name='delete-post'),
    path('<int:user_id>/all',  DeleteAllPosts.as_view(), name='delete-all'),
    path('<int:user_id>/<int:post_id>/update', UpatePost.as_view(), name='update-post'),
]
