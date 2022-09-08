from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SupportGroup, LocalGovt, GroupType


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SupportGroupForm(forms.ModelForm):
    class Meta:
        model = SupportGroup
        fields = '__all__'
