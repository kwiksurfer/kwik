from django import forms
from kwiksurfs.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        widgets = {
            'post': forms.Textarea(attrs={'cols': 40, 'rows': 2,})
        }
        fields = {'post','privacy',}

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        widgets = {
            'comment': forms.Textarea(attrs={'cols': 40, 'rows': 1,})
        }
        fields = {'comment',}
