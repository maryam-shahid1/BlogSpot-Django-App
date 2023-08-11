"""
This module contains forms for student authentication.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import User


class StudentSignUpForm(UserCreationForm):

    is_student = True
    is_organisation = False

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'organisation']

    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-input'}),
        'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        'email': forms.EmailInput(attrs={'class': 'form-input'}),
        'organisation': forms.TextInput(attrs={'class': 'form-input'}),
        'password': forms.PasswordInput(attrs={'class': 'form-input'}),
    }

    def save(self, commit=True):
        user = super(StudentSignUpForm, self).save(commit=True)
        user.is_student = True
        if commit:
            user.save()
        return user


class StudentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
