from django.contrib.auth.backends import ModelBackend

from mahi_auth.managers.get_user import get_user
from mahi_auth.models import User


class MahiAuthBackend(ModelBackend):
    """
    This auth backend authenticates users via a complex search for username,
    wherein the User instance is searched by the function ``get_user()``
    defined in the module ``mahi_auth.managers``.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user = get_user(username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
