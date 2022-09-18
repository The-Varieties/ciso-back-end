from django.urls import path
from . import views

urlpatterns = [
    path('data-vis-cpu/', views.get_data_vis_cpu, name='get_data_vis_cpu'),
    path('data-vis-ram/', views.get_data_vis_ram, name='get_data_vis_ram'),
]