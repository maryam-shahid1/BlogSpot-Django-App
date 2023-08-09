"""
This module contains views for student profile.
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from user.forms import StudentSignUpForm
from user.models import User


@login_required
def student_home(request):
    """
    Display the student's home page after successful login.

    ### Example Request:
        GET /home

    ### Example Response:
        Renders 'student_home.html' with user's first name.
    """
    first_name = request.user.first_name
    context = {'first_name': first_name.capitalize()}
    return render(request, 'blog/student_home.html', context)


@login_required
def student_profile(request):
    """
    Display the student's profile page.

    ### Example Request:
        GET /profile

    ### Example Response:
        Renders 'profile.html' with user's profile information.
    """
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'organisation': request.user.organisation
    }
    return render(request, 'blog/profile.html', context)


@login_required
def update_profile(request):
    """
    Handle the update of student profile information.

    ### Example Request:
        POST /update_profile
        {
            "email": maryam.shahid@gmail.com,
            "first_name": "Maryam",
            "last_name": "Shahid",
            "organisation": "Arbisoft",
            "password": maryam123
        }

    ### Example Response:
        Redirects to 'student_profile' upon successful update,
        or renders 'update_profile.html' with form errors.
    """
    current_user = User.objects.get(id=request.user.id)
    form = StudentSignUpForm(request.POST or None, instance=current_user)
    if form.is_valid():
        form.save()
        login(request, current_user)
        messages.success(request, 'Profile updated successfully!')
        return redirect('student_profile')
    return render(request, 'blog/update_profile.html', {'form': form})
