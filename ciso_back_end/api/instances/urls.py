from django.urls import path
from ciso_back_end.api.instances import views

urlpatterns = [
    path('instance/', views.instance, name='instance'),
    path('instance/<int:id>/', views.instance_by_id, name='instance_by_id'),
    path('prometheus-targets/', views.sync_prometheus, name='prometheus'),
]
