from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.managers import UserManager
from utils.validators import username_validator


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model for user table in database, with additional code for permission checks and user related methods.
    """

    username = models.CharField(
        verbose_name=_("username"),
        max_length=128,
        unique=True,
        help_text=_(
            "Required. Can contain Alfa Numeric characters only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_("Determines whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_(
            "Determines whether this user should be treated as active."
        ),
    )

    REQUIRED_FIELDS = ["password"]
    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username
