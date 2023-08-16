from django.contrib import admin
from .models import Category, Post, Users

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Users)