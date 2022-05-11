from django.urls import path
from userdata import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('users/',views.userApi),
    path('users/<int:id>/',views.userApi),
    path('prometheus-targets/', views.syncPrometheus2),
]