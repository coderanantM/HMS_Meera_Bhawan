from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmailAuthenticationForm, RegisterForm
from users.models import CustomUser  # Import CustomUser explicitly
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import credentials, auth
import json

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")  # Replace with your Firebase Admin SDK credentials
    firebase_admin.initialize_app(cred)

User = get_user_model()

def generate_unique_username(email):
    base_username = email.split('@')[0]
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username

@csrf_exempt
def auth_receiver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('id_token')
            email = data.get('email')

            # Verify Firebase ID Token
            decoded_token = auth.verify_id_token(id_token)
            if decoded_token['email'] != email:
                return JsonResponse({'success': False, 'error': 'Email mismatch'})

            # Validate BITS Email
            if not email.endswith('@pilani.bits-pilani.ac.in'):
                return JsonResponse({'success': False, 'error': 'Invalid email domain'})

            # Get or create user
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = generate_unique_username(email)
                user.user_type = 'STUDENT'
                user.set_unusable_password()  # No password for Google users
                user.save()

            # Set authentication backend and log in
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # Redirect to the appropriate dashboard
            return JsonResponse({'success': True, 'redirect_url': reverse('student_dashboard')})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required(login_url='login_view')
def student_dashboard(request):
    if request.user.user_type == 'STUDENT':
        return render(request, 'complaints/Page8.html')  # Render student dashboard
    else:
        return redirect('login_view')

@csrf_exempt
def firebase_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('id_token')

            # Verify Firebase ID Token
            decoded_token = auth.verify_id_token(id_token)
            email = decoded_token.get('email')

            # Validate BITS Email
            if not email.endswith('@pilani.bits-pilani.ac.in'):
                return JsonResponse({'success': False, 'error': 'Invalid email domain'})

            # Get or create user
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = generate_unique_username(email)
                user.user_type = 'STUDENT'
                user.set_unusable_password()  # No password for Google users
                user.save()

            # Set authentication backend and log in
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # Redirect to the appropriate dashboard
            return JsonResponse({'success': True, 'redirect_url': reverse('student_dashboard')})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request.user)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user using email and password
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect_dashboard(user)
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'users/Page1.html')

def redirect_dashboard(user):
    DASHBOARD_MAP = {
        'STUDENT': 'student_dashboard',
        'WARDEN': 'warden_dashboard',
        'SUPERINTENDENT': 'warden_dashboard',
        'EMS': 'ems_dashboard'
    }

    return redirect(reverse(DASHBOARD_MAP.get(user.user_type, 'home')))

@login_required(login_url='firebase_login')
def student_dashboard(request):
    if request.user.user_type == 'STUDENT':
        return render(request, 'complaints/Page8.html')  # Render dashboard
    else:
        return redirect('login_view')

@login_required(login_url='login_view')
def warden_dashboard(request):
    if request.user.user_type not in ['WARDEN', 'SUPERINTENDENT']:
        return redirect('home')
    return render(request, 'complaints/Page2.html')

@login_required
def ems_dashboard(request):
    if request.user.user_type != 'EMS':
        return redirect('home')
    return render(request, 'complaints/Page7.html')

def sign_out(request):
    logout(request)
    return redirect('login_view')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect(reverse('login_view'))

def signup_view(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request.user)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        user_type = request.POST.get('user_type')
        if form.is_valid():
            email = form.cleaned_data['email']
            username = generate_unique_username(email)
            name = form.cleaned_data['name']  # Get the name from the form
            user = form.save(commit=False)
            user.username = username
            user.name = name  # Save the name to the user instance
            user.user_type = user_type
            user.save()

            messages.success(request, "Registration successful. Please log in.")
            return redirect('login_view')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = RegisterForm()

    return render(request, 'users/signup.html', {'form': form})

def home_view(request):
    return render(request, 'users/Page1.html')