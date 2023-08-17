from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, logout
from .models import Post, Category, Users
from .serializers import PostSerializer, CategorySerializer, UserSerializer, RegistrationSerializer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes

class PostList(APIView):
    
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryList(APIView):
    

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryDetail(APIView):
   

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

class UserList(APIView):
   

    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    

    def get_object(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class PostsByCategory(APIView):
    def get(self, request, category_name):
        try:
            posts = Post.objects.filter(category__name=category_name)
            serialized_posts = PostSerializer(posts, many=True)
            return Response(serialized_posts.data)
        except Post.DoesNotExist:
            return Response({"message": "No posts found for this category"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_authentication(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    print(auth_header)
    if auth_header:
        token = auth_header.split(' ')[1]
        print(token)
        try:
            user = Token.objects.get(key=token).user
            print(user)
            if user.is_authenticated:
                return JsonResponse({'authenticated': True})
        except Token.DoesNotExist:
            pass
    
    return JsonResponse({'authenticated': False})

@api_view(["POST"])
@permission_classes([AllowAny])
def Register_Users(request):
    try:
        data =[]
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["message"] = "user registered successfully"
            data["email"] = account.email
            data["username"]= account.username
            data["first_name"] = account.first_name
            data["last_name"] = account.last_name
            data["token"] = token
        else:
            data = serializer.errors

        return Response(data)
    except IntegrityError as e:
        account = Users.objects.get(username='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})
    
    except KeyError as e:
        print(e)
        raise ValidationError({"400": f'Field {str(e)} missing'})
    
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    
    data ={}
    reqBody = json.loads(request.body)
    username = reqBody['username']
    password = reqBody['password']

    try:
        account = Users.objects.get(username=username)
    except Users.DoesNotExist:
        raise ValidationError({"400": "User not found"})
    
    token_tuple = Token.objects.get_or_create(user=account)
    token = token_tuple[0] if isinstance(token_tuple, tuple) else token_tuple

    if not check_password(password, account.password):
        raise ValidationError({"message": "Incorrect Login credentials"})
    
    if account:
        if account.is_active:
            login(request, account)
            data["message"] = "user logged in"
            data["username"] = account.username

            Res = {"data": data, "token": token.key}
            print(f'Authenticated: {request.user.is_authenticated}')
            return Response(Res)
        
        else:
            raise ValidationError({"400": "Account not active"})
    else:
        raise ValidationError({"400": "Account doesnt exist"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')
