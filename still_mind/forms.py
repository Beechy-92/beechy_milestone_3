from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'mood', 'summary', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title'
            }),
            'mood': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Calm, Grateful'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional short summary of this reflection...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your reflection...'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }