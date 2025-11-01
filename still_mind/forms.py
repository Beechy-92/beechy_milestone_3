from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'mood', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL-friendly name'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your reflection...'}),
            'mood': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Calm, Grateful'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }