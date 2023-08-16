from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('categories/<str:category_name>/', views.PostsByCategory.as_view(), name='posts-by-category'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.User_logout, name='logout'),
    path('posts/<int:pk>/comments/', include('comment.urls')),
    path('check-auth/', views.check_authentication, name='check-auth'),
    path('register-users', views.Register_Users, name='register_user'),
]

