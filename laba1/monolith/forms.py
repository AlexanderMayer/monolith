from django import forms
from django.contrib.auth.hashers import make_password
from django.forms import inlineformset_factory

from .models import *


class UserForm(forms.ModelForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'email', 'password', 'avatar']
        enctype = "multipart/form-data"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'content', 'photo']
        enctype = "multipart/form-data"


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['choice']


VoteFormSet = inlineformset_factory(
    parent_model=Post,
    model=Vote,
    form=VoteForm,
    fields=['choice'],
    extra=3,
    can_delete=False
)
