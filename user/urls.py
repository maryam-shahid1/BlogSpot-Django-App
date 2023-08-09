"""
URL patterns for student authentication and profile management.
"""

from django.urls import path

from user.views import authentication, profile

urlpatterns = [
    path('signup/', authentication.student_signup, name='student_signup'),
    path('login/', authentication.student_login, name='student_login'),
    path('home/', profile.student_home, name='student_home'),
    path('profile/', profile.student_profile, name='student_profile'),
    path('update-profile/', profile.update_profile, name='update_profile'),
    path('logout/', authentication.logout_request, name='logout_request'),
]
