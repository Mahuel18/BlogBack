from rest_framework import serializers
from .models import Category, Post, Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
    def create(self, validated_data):
        password = self.validated_data.pop("password")
        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

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