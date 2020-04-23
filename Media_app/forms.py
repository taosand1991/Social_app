from django.forms import DateInput, Textarea, TextInput, ImageField
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'email', 'password1', 'password2', 'location', 'date_of_birth', 'display_name', 'bio', 'image_url', 'gender'
        ]
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'image_url', 'location']

        widgets = {
            'bio': Textarea(attrs={'rows': 2, 'cols': 3, 'class': 'form-control'}),
            'location': TextInput(attrs={'placeholder': 'Location', 'class': 'form-control'}),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'post', 'picture'
        ]
        widgets = {
            'post': Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter post....', 'rows': 2, 'cols': 3})
        }


class EditPostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'post'
        ]
        widgets = {
            'post': Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter post...', 'rows': 2, 'cols': 3})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment'
        ]

        widgets = {
            'comment': Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment', 'rows': 5, 'cols': 6})
        }


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = [
            'name'
        ]
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Group name', 'Label': 'Group Name'})
        }

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self['name'].label = 'Group Name'


class GroupPostForm(ModelForm):
    class Meta:
        model = GroupPost
        fields = [
            'post'
        ]
        widgets = {
            'post': Textarea(attrs={'class': 'form-control', 'placeholder': 'Write post...', 'rows': 2, 'cols': 3})
        }