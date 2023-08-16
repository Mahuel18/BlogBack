from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from blog.models import Post
from .serializers import CommentSerializer

class CommentList(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)  # Obtener el post relacionado
        comments = Comment.objects.filter(post=post)  # Filtrar comentarios por el post
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)  # Asignar el post al comentario
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)