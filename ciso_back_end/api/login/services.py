from ..users.models import *

def authentice_user(username, password):
    user = User.objects.get(user_username=username, user_password=password)
    if user:
        return user.user_id
    return None