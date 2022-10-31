import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import *
from ..users.models import User
from ..instances.models import Instances


@api_view(['POST'])
def instance_type(request):
    data = json.loads(str(request.body.decode('utf-8')).replace("'", '"'))
    user = User.objects.get(user_id=data['user_id'])
    instance = Instances.objects.get(instance_id=data['instance_id'])
    change_instance_type(user.user_aws_access_key,
                         user.user_aws_secret_key,
                         instance.instance_aws_id,
                         data['target_instance_type'])
    instance.instance_type = data['target_instance_type']
    instance.save()

    return Response(status=status.HTTP_200_OK)

