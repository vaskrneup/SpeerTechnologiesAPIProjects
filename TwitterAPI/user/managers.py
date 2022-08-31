from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager that omits email during user creation from terminal.
    """

    def create_user(self, username: str, password: str, **additional_fields):
        """
        Creates user from the given username and password.

        :param username: username for the new user.
        :param password: raw password for the new user. It will be securely stored by the function.
        :param additional_fields: Additional parameters to pass to the model.
        :return: newly created user.
        """

        if not username:
            raise ValueError(_("Username is required."))

        user = self.model(username=username, **additional_fields)
        user.set_password(raw_password=password)
        user.save()

        return user

    def create_superuser(self, username: str, password: str, **additional_fields):
        """
        Creates user with all the permissions from the given username and password.

        :param username: username for the new user.
        :param password: raw password for the new user. It will be securely stored by the function.
        :param additional_fields: Additional parameters to pass to the model.
        :return: newly created user.
        """

        return self.create_user(
            username=username,
            password=password,
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **additional_fields
        )
