from django.urls import path
from . import views

urlpatterns = [
    path('data-vis/', views.get_data_vis, name='data-vis-cpu'),
]