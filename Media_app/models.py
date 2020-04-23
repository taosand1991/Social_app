from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ('M', 'MALE'),
    ('F', 'FEMALE'),
)


class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField('Email Address', unique=True)
    location = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    image_url = models.ImageField(upload_to='image/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=100)
    friends = models.ManyToManyField('self', related_name='friends')
    friend_requests = models.ManyToManyField('self', related_name='friend_requests')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'display_name']

    def __str__(self):
        return self.display_name


class Notification(models.Model):
    sender = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Post(models. Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes')
    picture = models.ImageField(upload_to='per_image/', blank=True, null=True)

    def __str__(self):
        return f'{self.author.display_name}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.display_name}'


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    member = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author


class CommentGroup(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.display_name

