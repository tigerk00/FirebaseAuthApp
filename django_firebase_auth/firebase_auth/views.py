import json

import firebase_admin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from pyrebase import pyrebase
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from .exceptions import NoUserError
from .models import User
from .serializers import AuthTokenSerializer, UserRegisterSerializer, UserSerializer

with open('firebase_app_creds.json') as d:
    config = json.load(d)
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()


class AuthRegister(generics.CreateAPIView):
    """Register new user in firebase and add him to our local DB"""
    authentication_classes = ()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["auth"] = auth
        return context


class CreateTokenView(ObtainAuthToken):
    """Creates a new firebase auth id token for user."""
    authentication_classes = ()
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        new_id_token = auth.refresh(user.refresh_token)['idToken']
        return Response({'token': new_id_token})


class CurrentUserInfoView(generics.RetrieveAPIView):
    """Current authenticated user info"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserView(APIView):
    """READ-UPDATE-DELETE operations on User model"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_object(self, pk):
        return User.objects.get(pk=pk)

    def get(self, request, pk):
        """Retrieves data of specific user from local DB(Only for admin users)"""
        try:
            instances = User.objects.get(pk=pk)
            serializer = UserSerializer(instances, many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise NoUserError()

    def patch(self, request, pk):
        """Updates the info of a specific user in local DB and Firebase list of users(Only for admin users)"""

        # Local DB level
        instance = self.get_object(pk)
        serializer = UserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Firebase level
        validated_data = serializer.validated_data
        updated_validated_data = {"uid": instance.uid}
        for key in list(validated_data):
            if key in ['email', 'phone_number', 'password', 'username', 'photo_url']:
                if validated_data.get(key) is not None and validated_data.get(key) != '':
                    updated_validated_data[key] = validated_data.get(key)

        if 'username' in updated_validated_data:
            updated_validated_data['display_name'] = updated_validated_data.pop('username')

        if len(updated_validated_data) > 1:
            firebase_admin.auth.update_user(**updated_validated_data)
            # Refresh tokens expire when a major account change is detected for the user.
            # This includes events like password or email address updates(Source: Docs).
            if 'email' in updated_validated_data or 'password' in updated_validated_data:
                cust_token = firebase_admin.auth.create_custom_token(instance.uid)
                user = auth.sign_in_with_custom_token(cust_token.decode())
                instance.refresh_token = user['refreshToken']
                instance.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        """Deletes user from local DB and Firebase list of users(Only for admin users)"""
        try:
            instance = User.objects.get(id=pk)
            firebase_admin.auth.delete_user(instance.uid)
            instance.delete()
            return HttpResponse(f"User with id={pk} was deleted from local DB and Firebase users list successfully !")
        except ObjectDoesNotExist:
            raise NoUserError()


class UsersListView(APIView):
    """Retrieves list of all users from local DB(Only for admin users)"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request, format=None):
        instances = User.objects.all()
        serializer = UserSerializer(instances, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
@permission_classes((permissions.IsAuthenticated, permissions.IsAdminUser))
def users_list_firebase(request):
    users = {}
    for user in firebase_admin.auth.list_users().iterate_all():
        if user.email is not None:
            users[user.email] = user.uid
    return JsonResponse(users)