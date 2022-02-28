from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(label="", required=False, widget=forms.Textarea(
        attrs={
            'placeholder' : '생각은 짧게라도 반드시 적어둬야 해요',
            'rows' : 4,
        }
    ))
    class Meta:
        model = Comment
        fields = ('author', 'body',)

class SearchForm(forms.Form):
    WHICH = (
        ('title', '책 제목'),
        ('author','저자'),
        ('body', '내용')
    )

    search_keyword = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs = {
            'placeholder' : '찾고야 말 테다',
            'class' : 'search-form'
        }
    ))
    which = forms.ChoiceField(label="", required=False, choices=WHICH, 
        widget=forms.Select(
            attrs= {
                # 'class' : 'dropdown'
            }
        )
    )
    class Meta: 
        fields = ('search_keyword', 'which')