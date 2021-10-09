from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Accountuser
class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Accountuser
        fields = ['username','email','password','phonenum']

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = Accountuser
        fields = ['username','email','password','phonenum']