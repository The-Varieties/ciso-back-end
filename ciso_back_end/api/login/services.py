from multiprocessing import AuthenticationError
from rest_framework import status

from ..users.models import *
from ...commons.utils import generate_token


def authenticate_user(username, password):
    try:
        user = User.objects.get(user_username=username, user_password=password)
        token = generate_token(user.user_id)
        return token
    except User.DoesNotExist:
        return None
