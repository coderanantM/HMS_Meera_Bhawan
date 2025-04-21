# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        if not username:
            username = email.split('@')[0]  # Generate username from email prefix

        extra_fields.setdefault('user_type', 'STUDENT')

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Allow setting superuser's `user_type`
        if 'user_type' not in extra_fields:
            extra_fields['user_type'] = 'SUPERINTENDENT'  # Default for superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('STUDENT', 'Student'),
        ('WARDEN', 'Warden'),
        ('SUPERINTENDENT', 'Superintendent'),
        ('EMS', 'EMS Team'),
    )

    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='STUDENT')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Removes username requirement

    def __str__(self):
        return self.email
