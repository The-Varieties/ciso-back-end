from multiprocessing import AuthenticationError

from ..users.models import *
from ...commons.utils import generate_token


def authenticate_user(username, password):
    user = User.objects.get(user_username=username, user_password=password)
    if user:
        token = generate_token(user.user_id)
        return token
    raise AuthenticationError()
