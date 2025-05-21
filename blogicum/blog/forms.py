from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment, User


User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )
