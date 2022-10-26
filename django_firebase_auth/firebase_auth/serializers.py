from django.contrib.auth import (
    authenticate
)
from django.contrib.auth.hashers import make_password
from .models import User
from django.utils.translation import gettext as _
from rest_framework import serializers
import firebase_admin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'required': False, 'write_only': True, 'min_length': 8},
            'username': {'required': False},
            'email': {'required': False},
            'uid': {'read_only': True},
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'refresh_token': {'read_only': True},
            'user_permissions': {'read_only': True},
            'groups': {'read_only': True},
        }

    def update(self, instance, validated_data):
        updated_validated_data = {}
        for key in list(validated_data):
            if validated_data.get(key) is not None and validated_data.get(key) != '':
                    updated_validated_data[key] = validated_data.get(key)

        user = super().update(instance, updated_validated_data)

        if "password" in updated_validated_data.keys():
            user.set_password(updated_validated_data['password'])
            user.save()

        return user


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'username']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def create(self, validated_data):
        auth = self.context.get("auth")
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')

        user = auth.create_user_with_email_and_password(email, password)
        decoded_token = firebase_admin.auth.verify_id_token(user['idToken'])
        uid = decoded_token.get("uid")
        auth.send_email_verification(user['idToken'])
        refresh_token = user.get('refreshToken')
        return User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            uid=uid,
            refresh_token=refresh_token
        )


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
