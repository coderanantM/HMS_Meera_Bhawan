import firebase_admin
from firebase_admin import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()

class FirebaseAuthenticationBackend(BaseBackend):
    def authenticate(self, request, token=None):
        try:
            # Verify the Firebase ID token
            decoded_token = auth.verify_id_token(token)
            email = decoded_token.get('email')

            # Check if the email is a BITS student email (starts with f20XX)
            if email and email.startswith('f20') and email.endswith('@pilani.bits-pilani.ac.in'):
                # Get or create the user
                user, created = User.objects.get_or_create(email=email)
                if created:
                    user.username = email.split('@')[0]
                    user.user_type = 'STUDENT'  # Set user type to STUDENT
                    user.save()
                return user
        except Exception as e:
            print(f"Firebase authentication error: {e}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None