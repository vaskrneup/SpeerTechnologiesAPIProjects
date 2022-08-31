from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def username_validator(username: str) -> None:
    """
    raises `django.core.exceptions.ValidationError` if the given username is not alfa-numeric.

    :param username: Text to validate
    :return: None
    """

    if not username.isalnum():
        raise ValidationError(_("Username can only contain alphabets or numbers."))
