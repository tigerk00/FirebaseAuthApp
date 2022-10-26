import firebase_admin
from django.contrib.auth.hashers import make_password
from .models import User
from .views import auth
from django.contrib.auth.management.commands import createsuperuser


def create_super_user(email, password, username=None):
    firebase_user = auth.create_user_with_email_and_password(email, password)
    decoded_id_token = firebase_admin.auth.verify_id_token(firebase_user['idToken'])
    uid = decoded_id_token.get("uid")
    refresh_token = firebase_user.get('refreshToken')
    User.objects.create_user(
        username=username,
        email=email,
        password=password,
        uid=uid,
        refresh_token=refresh_token,
        is_staff=True,
        is_superuser=True,
    )