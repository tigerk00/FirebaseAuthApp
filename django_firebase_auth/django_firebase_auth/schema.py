from drf_spectacular.extensions import OpenApiAuthenticationExtension
from django.utils.translation import gettext_lazy as _


class FireBaseTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'firebase_auth.authentication.FirebaseAuthentication'
    name = "AuthToken"

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': _(
                'Firebase Token-based authentication with required prefix "%s"'
            ) % "Token"
        }