from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status

from .serializer import PostSerializer
from .models import Post
from account.models import CustomUser
class CreatePostView(CreateAPIView):
    '''
    API for creating posts
    '''
    serializer_class = PostSerializer

    def create(self, request):
        postSerializer = PostSerializer(data=request.data)
        if postSerializer.is_valid():
            get_object_or_404(CustomUser, pk=request.data.get('author'))
            postSerializer.save() 
            return Response(postSerializer.data, status=status.HTTP_201_CREATED)
        return Response(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetPosts(ListAPIView):
    '''
    API for getting all the posts associated with a specific user
    '''
    serializer_class = PostSerializer
    def get_queryset(self):
        user_id =  self.kwargs['user_id']
        return Post.objects.filter(author=user_id)


class DeletePost(DestroyAPIView):
    '''
    API for deleting a post
    '''
    serializer_class = PostSerializer
    def delete(self, request, user_id, post_id):

        post = get_object_or_404(Post, id=post_id, author=user_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteAllPosts(DestroyAPIView):
    '''
    API for deleting all posts for a particular user
    '''
    serializer_class = PostSerializer
    def delete(self, request, user_id):
        posts = get_list_or_404(Post, author=user_id)
        for post in posts:
            post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpatePost(UpdateAPIView):
    '''
    API to update a post
    '''
    serializer_class = PostSerializer

    def put(self, request, user_id, post_id):
        post = get_object_or_404(Post, id=post_id, author=user_id)
        postSerializer = PostSerializer(post, data=request.data)
        if postSerializer.is_valid():
            postSerializer.save() 
            return Response(postSerializer.data)
        return Response(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)