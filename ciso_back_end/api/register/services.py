from ..users.models import *

def authentice_user(username, firstname, lastname, email, password):
    user = User.objects.get(user_username=username, user_firstname=firstname, user_lastname=lastname, user_email=email, user_password=password)
    if user:
        return user.user_id
    return None