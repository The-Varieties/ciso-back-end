from django.urls import path
from . import views

urlpatterns = [
    path('get-cpu-usage/', views.get_cpu_usage),
    path('get-ram-usage/', views.get_ram_usage),
    path('get-server-info/', views.get_server_info)
]
