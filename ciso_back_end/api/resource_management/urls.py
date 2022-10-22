from django.urls import path
from ciso_back_end.api.resource_management import views

urlpatterns = [
    path('change-type/', views.instance_type, name='change_instance_type')
]
