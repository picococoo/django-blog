from django import forms

from django_markdown.widgets import MarkdownWidget

from .models import BlogPost


class PostForm(forms.ModelForm):
    title = forms.CharField(label='标题',
                            max_length=200)
    body = forms.CharField(label='正文',
                           widget=MarkdownWidget)

    class Meta:
        model = BlogPost
        fields = ('title', 'body')
