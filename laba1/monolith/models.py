from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    username = models.CharField(max_length=254, verbose_name='Логин', blank=False, unique=True)
    email = models.EmailField(verbose_name='Почта', blank=False, unique=True)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='photo', blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Post(models.Model):
    name = models.CharField(max_length=254, verbose_name='Название поста', blank=False)
    content = models.TextField(blank=True, default=" ", null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    photo = models.ImageField(verbose_name='Фото', upload_to='photo', null=True, blank=True)

    def was_published_recently(self):
        return self.date_created >= timezone.now() - datetime.timedelta(hours=1)

    def __str__(self):
        return self.name


class Vote(models.Model):
    choice = models.CharField(max_length=254, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Название поста', null=False)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice


class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
