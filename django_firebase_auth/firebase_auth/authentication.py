from django.core.exceptions import ObjectDoesNotExist
from .models import User
from rest_framework import authentication
import firebase_admin.auth as auth
from firebase_admin import credentials, initialize_app
from .exceptions import NoAuthToken, InvalidAuthToken, FirebaseError, NoUserError

class FirebaseAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request, username=None, password=None):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        user_info = auth.get_user(uid)

        try:
            user = User.objects.get(email=user_info.email, uid=uid)
            return (user, None)
        except ObjectDoesNotExist:
            raise NoUserError()




