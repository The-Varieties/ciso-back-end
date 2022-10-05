<<<<<<< HEAD
from ..users.models import *

def authentice_user(username, password):
    user = User.objects.get(user_username=username, user_password=password)
    if user:
        return user.user_id
    return None
=======
from multiprocessing import AuthenticationError

from ..users.models import *
from ...commons.utils import generate_token


def authenticate_user(username, password):
    user = User.objects.get(user_username=username, user_password=password)
    if user:
        token = generate_token(user.user_id)
        return token
    raise AuthenticationError()
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
