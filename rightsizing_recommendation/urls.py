from django.urls import path
from . import views

urlpatterns = [
    path('get-cpu-usage/', views.get_cpu_usage, name='get-cpu-usage'),
    path('get-ram-usage/', views.get_ram_usage, name="get-ram-usage"),
    path('get-server-info/', views.get_server_info, name="get-server-info"),
    path('get-usage-category/', views.get_usage_classifier, name="get-usage-category"),
    path('get-x/', views.get_rx, name="get-rx")
]
