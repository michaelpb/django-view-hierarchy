from django import forms
from microblog.models import Author, Follow, MicroPost


class MicroPostForm(forms.ModelForm):
    class Meta:
        model = MicroPost
        fields = ['author', 'title', 'body']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']


class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['author', 'follower']
