from django import forms

from users.models import CustomUser
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('birthday',)