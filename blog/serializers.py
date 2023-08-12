from rest_framework import serializers
from .models import User, Category, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'paragraph1', 'paragraph2', 'paragraph3', 
                  'paragraph4', 'paragraph5', 'introduction', 'category', 'image', 'created_at', 'author']