from django.db.models import Q

from mahi_auth.models import User


def get_user(username):
    """
    Get the user corresponding to the given username

    :param username: the username provided to identify the user
    :return: the user, if a user with the given username is found
    :raise: User.DoesNotExist, if no user with the given username is found
    """

    try:
        q_username = Q(username=username)
        q_email = Q(email=username)
        q_phone_number = Q(phone_number=username)
        q = q_username | q_email | q_phone_number
        user = User.objects.get(q)
        return user
    except User.DoesNotExist:
        pass
    raise User.DoesNotExist
