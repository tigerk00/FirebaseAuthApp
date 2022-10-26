from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    uid = models.CharField(unique=True, max_length=150, default='uid_default_val',
                           help_text=_("Unique value that user gets from firebase after registration"),)
    refresh_token = models.TextField(
        default='ref_token_default_val',
        help_text=_("Refresh token is used to retrieve new ID tokens for Firebase auth. It is expires only if the user is disabed, deleted or has major account change"),)
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=50, null=True)
    photo_url = models.CharField(max_length=200, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-pk']
