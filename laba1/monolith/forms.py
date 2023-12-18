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


class VoteForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название опроса')
    content = forms.CharField(max_length=2000, widget=forms.Textarea(), label='Описание опроса')
    photo = forms.ImageField(label='Фото для опроса')
    choice1 = forms.CharField(max_length=100, label='Вариант 1')
    choice2 = forms.CharField(max_length=100, label='Вариант 2')
    choice3 = forms.CharField(max_length=100, label='Вариант 3')
