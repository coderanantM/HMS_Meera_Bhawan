from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'bhavan', 'room', 'contact_no', 'complaint_group',
            'area', 'requirement', 'category', 'comments', 'time'
        ]
