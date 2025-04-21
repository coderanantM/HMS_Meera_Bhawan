from django.db import models
from django.conf import settings
from django.utils import timezone
import pytz

class Complaint(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE  # Automatically delete complaints when the user is deleted
    )
    bhavan = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=15)
    complaint_group = models.CharField(max_length=50, choices=[("Common", "Common"), ("Room", "Room")])
    area = models.CharField(max_length=255, null=True, blank=True)
    requirement = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    preferred_time = models.CharField(max_length=100, blank=True, null=True)
    ems_status = models.CharField(max_length=20, default="Pending")

    ist = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.bhavan} - {self.room}"
    
class TechnicalManager(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name