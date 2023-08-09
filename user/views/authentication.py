"""
This module contains views for student authentication.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from user.forms import StudentLoginForm, StudentSignUpForm


def student_signup(request):
    """
    Handle the student signup process.

    ### Example Request:
        POST /signup
        {
            "email": maryam.shahid@gmail.com,
            "first_name": "Maryam",
            "last_name": "Shahid",
            "organisation": "Arbisoft"
        }

    ### Example Response:
        Redirects to 'student_login' upon successful signup
        or renders 'student_signup.html' with form errors.
    """
    if request.user.is_authenticated:
        return redirect('student_home')

    form = None
    try:
        if request.method == 'POST':
            form = StudentSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Registered Successfully!')
                return redirect('student_login')
        else:
            form = StudentSignUpForm()
    except Exception as error:
        messages.error(request, f'An error occurred: {error}')

    context = {'form': form}
    return render(request, 'blog/student_signup.html', context)


def student_login(request):
    """
    Handle the student login process.

    ### Example Request:
        POST /login
        {
            "email": maryam.shahid@gmail.com,
            "password": maryam123
        }

    ### Example Response:
        Redirects to 'student_home' upon successful login,
        or renders 'student_login.html' with form errors.
    """
    if request.user.is_authenticated:
        return redirect('student_home')

    form = None
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user and user.is_student:
                login(request, user)
                return redirect('student_home')
            else:
                messages.error(request, 'Invalid credentials!')
    else:
        form = StudentLoginForm()

    context = {'form': form}
    return render(request, 'blog/student_login.html', context)


@login_required
def logout_request(request):
    """
    Handle the student logout process.

    ### Example Request:
        GET /logout

    ### Example Response:
        Redirects to 'student_login' after logging out.
    """
    logout(request)
    return redirect('student_login')
