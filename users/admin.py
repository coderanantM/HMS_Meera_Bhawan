# admin.py in the 'users' app
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')  # Adjust fields as necessary
    search_fields = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)

