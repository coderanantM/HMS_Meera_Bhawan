from django.shortcuts import redirect
from django.urls import reverse

def set_user_type(strategy, details, user=None, *args, **kwargs):
    if user and not user.user_type:
        email = user.email
        if email.endswith('@pilani.bits-pilani.ac.in'):
            user.user_type = 'STUDENT'
            user.save()
    return {'user': user}
