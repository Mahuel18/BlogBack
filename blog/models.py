from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, first_name=None, last_name=None, is_staff = None, is_superuser= None):
        if not username:
            raise ValueError('Username must be provided')
        user = self.model(
            username=username, 
            email = email,
            first_name=first_name,
            last_name=last_name,
            is_staff = is_staff,
            is_superuser = is_superuser
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('first_name', 'Null')
        extra_fields.setdefault('last_name', 'Null')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class Users(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True, default=None)  # Cambio aquí
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = MyAccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label): 
        return self.is_superuser

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    introduction = models.TextField()
    paragraph1 = models.TextField()
    paragraph2 = models.TextField()
    paragraph3 = models.TextField()
    paragraph4 = models.TextField()
    paragraph5 = models.TextField()
    image = models.ImageField(upload_to='media')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
