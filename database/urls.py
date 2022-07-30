from django.urls import path
from database import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('instance/',views.instance, name='instance'),
    path('instance/<int:id>/',views.instanceById, name='instance_by_id'),
    path('prometheus-targets/', views.syncPrometheus, name='prometheus'),
]