from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.timezone import now as django_now  # Rename the Django timezone function
import pytz  # Keep the pytz import for timezone conversion
import datetime  # For the module

import json
from complaints.models import Complaint

from datetime import datetime  # For the class
def complaint_form_student(request):
    if request.method == 'POST':
        # Process form data
        bhavan = request.POST.get('bhavan')
        room = request.POST.get('room')
        contact_no = request.POST.get('contactNo')
        complaint_group = request.POST.get('complaintGroup')
        area = request.POST.get('area', '')
        requirement = request.POST.get('requirement')
        category = request.POST.get('category', '')
        preferred_time = request.POST.get('preferredTime', '')
        comments = request.POST.get('comments', '')

        # Get current time in UTC and convert to IST
        utc_now = django_now()  # Use the renamed Django timezone function
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))  # Convert to IST

        # Save the complaint to the database
        Complaint.objects.create(
            bhavan=bhavan,
            room=room,
            contact_no=contact_no,
            complaint_group=complaint_group,
            area=area,
            requirement=requirement,
            category=category,
            preferred_time=preferred_time,
            comments=comments,
            user=request.user,  # Store the logged-in user who submitted the complaint
            ist=ist_now  # Set the IST field
        )

        # Redirect to the student dashboard
        return redirect('student_dashboard')  # This should be a URL name for the student dashboard

    # If the request is GET, render the form
    context = {
        'requirement_options': ["electrical", "Mason", "Carpentry", "Painter", "Sweeper", "Worker"],
        'time_options': [
            {"value": "2-3", "label": "2-3 pm"},
            {"value": "3-4", "label": "3-4 pm"},
            {"value": "4-5", "label": "4-5 pm"}
        ],
        'category_options': []  # Dynamically set based on the requirement
    }

    return render(request, 'complaints/Page8.html', context)

def complaint_form_warden(request):
    if request.method == 'POST':
        # Process form data
        bhavan = request.POST.get('bhavan')
        room = request.POST.get('room')
        contact_no = request.POST.get('contactNo')
        complaint_group = request.POST.get('complaintGroup')
        area = request.POST.get('area', '')
        requirement = request.POST.get('requirement')
        category = request.POST.get('category', '')
        preferred_time = request.POST.get('preferredTime', '')
        comments = request.POST.get('comments', '')

        # Get current time in UTC and convert to IST
        utc_now = django_now()  # Use the renamed Django timezone function
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))

        # Save the complaint to the database
        Complaint.objects.create(
            bhavan=bhavan,
            room=room,
            contact_no=contact_no,
            complaint_group=complaint_group,
            area=area,
            requirement=requirement,
            category=category,
            preferred_time=preferred_time,
            comments=comments,
            user=request.user,  # Store the logged-in user who submitted the complaint
            ist=ist_now  # Set the IST field
        )

        # Use messages framework to display a success message
        messages.success(request, 'Your complaint has been submitted successfully!')

        # Redirect to the warden dashboard
        return redirect('warden_dashboard')  # This should be a URL name for the warden dashboard

    # If the request is GET, render the form
    context = {
        'requirement_options': ["electrical", "Mason", "Carpentry", "Painter", "Sweeper", "Worker"],
        'time_options': [
            {"value": "2-3", "label": "2-3 pm"},
            {"value": "3-4", "label": "3-4 pm"},
            {"value": "4-5", "label": "4-5 pm"}
        ],
        'category_options': []  # Dynamically set based on the requirement
    }

    return render(request, 'complaints/Page2.html', context)

def complaint_success(request):
    return render(request, 'complaints/complaint_success.html')

def team_info_warden(request):
    incharge = {
        'name': 'XYZ',
        'designation': 'Hostel Incharge',
        'email': 'xyz@gmail.com',
        'phone': '7023714156',
    }

    technical_manager = {
        'name': 'XYZ',
        'designation': 'Technical Manager',
        'email': 'xyz@gmail.com',
        'phone': '7023714156',
    }

    context = {
        'incharge': incharge,
        'technical_manager': technical_manager,
    }

    return render(request, 'complaints/Page5.html', context)

def team_info_student(request):
    incharge = {
        'name': 'XYZ',
        'designation': 'Hostel Incharge',
        'email': 'xyz@gmail.com',
        'phone': '7023714156',
    }

    technical_manager = {
        'name': 'XYZ',
        'designation': 'Technical Manager',
        'email': 'xyz@gmail.com',
        'phone': '7023714156',
    }

    context = {
        'incharge': incharge,
        'technical_manager': technical_manager,
    }

    return render(request, 'complaints/Page10.html', context)

@login_required
def complaints_view(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    context = {'complaints': complaints}
    return render(request, 'complaints/Page9.html', context)

from pytz import timezone
def format_time_am_pm(time_str):
    """
    Converts a time string (e.g., '14:30') to 12-hour format with AM/PM (e.g., '2:30 PM').
    Handles cases where the time is already in a readable format like '2-3 pm'.
    """
    if not time_str:
        return 'N/A'
    try:
        # Handle cases where the time is already in a readable format (e.g., '2-3 pm')
        if 'am' in time_str.lower() or 'pm' in time_str.lower():
            return time_str  

        
        from datetime import datetime
        time_obj = datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%I:%M %p')  
    except ValueError:
        return time_str  

@login_required
def fetch_student_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    complaints_data = [
        {
            'id': complaint.id,
            'IST': complaint.ist.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d %b %Y %H:%M:%S') if complaint.ist else 'N/A',
            'name': complaint.user.name,  # Fetch the name from the user model
            'bitsId': complaint.user.email,
            'contact_no': complaint.contact_no,
            'room': complaint.room,
            'area': complaint.area,
            'requirement': complaint.requirement,
            'category': complaint.category,
            'preferred_time': format_time_am_pm(complaint.preferred_time),  # Format time in AM/PM
            'description': complaint.comments,
            'status': "In Progress" if complaint.status == "Sent to EMS" else complaint.status,
        }
        for complaint in complaints
    ]
    return JsonResponse(complaints_data, safe=False)

@login_required
def fetch_warden_complaints(request):
    complaints = Complaint.objects.filter(user__user_type__in=['WARDEN', 'SUPERINTENDENT']).order_by('-created_at')
    complaints_data = [
        {
            'id': complaint.id,
            'IST': complaint.ist.astimezone(timezone('Asia/Kolkata')).strftime('%d %b %Y %I:%M:%S %p') if complaint.ist else 'N/A',
            'name': complaint.user.email.split('@')[0].capitalize(),
            'bitsId': complaint.user.email,
            'contact_no': complaint.contact_no,
            'room': complaint.room,
            'area': complaint.area,
            'requirement': complaint.requirement,
            'category': complaint.category,
            'preferred_time': format_time_am_pm(complaint.preferred_time),  # Format time in AM/PM
            'description': complaint.comments,
            'status': complaint.status,
        }
        for complaint in complaints
    ]
    return JsonResponse(complaints_data, safe=False)

@login_required
def fetch_student_complaints_for_warden(request):
    # Fetch complaints submitted by all users with the STUDENT user type
    complaints = Complaint.objects.filter(user__user_type='STUDENT').order_by('-created_at')
    complaints_data = [
        {
            'id': complaint.id,
            'IST': complaint.ist.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d %b %Y %H:%M:%S') if complaint.ist else 'N/A',
            'name': complaint.user.get_full_name(),
            'bitsId': complaint.user.username,
            'contact_no': complaint.contact_no,
            'room': complaint.room,
            'area': complaint.area,
            'requirement': complaint.requirement,
            'category': complaint.category,
            'preferred_time': complaint.preferred_time,
            'description': complaint.comments,
            'status': complaint.status,
            'ems_status': complaint.ems_status, # Fetch the updated status
        }
        for complaint in complaints
    ]
    return JsonResponse(complaints_data, safe=False)

@login_required
def send_warden_complaints_to_ems(request):
    """
    Automatically send all previous complaints of the warden to EMS.
    """
    try:
        # Fetch all complaints of the warden
        complaints = Complaint.objects.filter(user__user_type__in=['WARDEN', 'SUPERINTENDENT'], status="Pending")

        # Update the status of each complaint to "Sent to EMS"
        complaints.update(status="Sent to EMS")

        return JsonResponse({'success': True, 'message': 'All previous complaints of the warden have been sent to EMS.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def fetch_active_complaints(request):
    """
    Fetch complaints with statuses that should remain visible in the EMS dashboard.
    """
    send_warden_complaints_to_ems(request)
    
    complaints = Complaint.objects.filter(status__in=['Sent to EMS', 'In Progress']).order_by('-created_at')
    complaints_data = [
        {
            'id': complaint.id,
            'IST': complaint.ist.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d %b %Y %I:%M:%S %p') if complaint.ist else 'N/A',
            
            'bhavan': complaint.bhavan,
            'room': complaint.room,
            'requirement': complaint.requirement,
            'category': complaint.category,
            'preferred_time': complaint.preferred_time,
            'description': complaint.comments,
            'status': complaint.status,
        }
        for complaint in complaints
    ]
    return JsonResponse(complaints_data, safe=False)


@login_required
def previous_student_complaints(request):
    complaints = Complaint.objects.filter(user__user_type='STUDENT').order_by('-created_at')
    context = {'complaints': complaints}
    return render(request, 'complaints/Page9.html', context)

@login_required
def previous_warden_complaints(request):
    complaints = Complaint.objects.filter(user__user_type__in=['WARDEN', 'SUPERINTENDENT']).order_by('-created_at')
    context = {'complaints': complaints}
    return render(request, 'complaints/Page4.html', context)

def page3(request):
    return render(request, 'complaints/Page3.html')

def page2(request):
    return render(request, 'complaints/Page2.html')

def page6(request):
    return render(request, 'complaints/Page6.html')

def page7(request):
    return render(request, 'complaints/Page7.html')

@csrf_exempt
@login_required
def update_status_for_all_dashboards(request):
    """
    Handles status updates for complaints in the Warden Dashboard.
    Updates the status to 'Sent to EMS' or 'In Progress' based on the action.
    """
    if request.method == 'POST':
        try:
            complaint_id = request.POST.get('complaint_id')
            new_status = request.POST.get('new_status')  # Get the new status from the request

            # Fetch the complaint
            complaint = Complaint.objects.get(id=complaint_id)

            # Update the status based on the action
            if new_status == "Sent to EMS":
                complaint.status = "Sent to EMS"
                complaint.ems_status = "Pending"  # Update the EMS status as well
            elif new_status == "In Progress":
                complaint.status = "In Progress"
                complaint.ems_status = "In Progress" 

            complaint.save()

            return JsonResponse({
                'success': True,
                'message': f'Status updated to {complaint.status}.',
                'updated_status': complaint.status
            })
        except Complaint.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Complaint not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
@login_required
def update_ems_status_and_student_status(request):
    """
    Updates the EMS Status to 'In Progress' and the Student Dashboard Status to 'In Progress'
    when the Approve button is clicked in the EMS Dashboard.
    """
    if request.method == 'POST':
        try:
            complaint_id = request.POST.get('complaint_id')

            # Fetch the complaint
            complaint = Complaint.objects.get(id=complaint_id)

            # Update the EMS Status and the main status
            complaint.ems_status = "In Progress"
            complaint.status = "In Progress"
            complaint.save()

            return JsonResponse({'success': True, 'message': 'EMS Status updated to In Progress.'})
        except Complaint.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Complaint not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)