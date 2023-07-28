from django import forms
from .models import Post, Category
from django.forms.widgets import CheckboxSelectMultiple

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text_type'].help_text = 'Please select post category'

    class Meta:
        model = Post
        fields = ['author', 'title', 'text_type', 'text']
        widgets = {
            'title': forms.Textarea(attrs={'cols': 120, 'rows': 1}),
            'text': forms.Textarea(attrs={'cols': 120, 'rows': 8}),
        }

class SubscribeForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple,

    )
