from django.contrib.auth.models import User
from django import forms




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password']


