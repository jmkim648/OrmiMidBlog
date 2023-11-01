from django import forms
from .models import Post, Comment, Tag, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'thumb_image', 'category', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']