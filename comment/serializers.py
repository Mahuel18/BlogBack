from rest_framework import serializers
from .models import Comment
from blog.models import Users



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'first_name', 'last_name']

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['content', 'created_at', 'author', 'post']

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment