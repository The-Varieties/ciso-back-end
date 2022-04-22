from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from database.models import Instance
from database.serializers import InstanceSerializer
from django.core.files.storage import default_storage

# Create your views here.
@csrf_exempt
def instanceApi(request,id=0):
    if request.method=='GET':
        instance = Instance.objects.all()
        instance_serializer=InstanceSerializer(instance,many=True)
        return JsonResponse(instance_serializer.data,safe=False)
    elif request.method=='POST':
        instance_data=JSONParser().parse(request)
        instance_serializer=InstanceSerializer(data=instance_data)
        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='DELETE':
        instance=Instance.objects.get(Instanceid=id)
        instance.delete()
        return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
def SaveFile(request):
    file=request.FILES['file']
    file_name=default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False)