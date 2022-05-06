from django.urls import path
from database import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('user/',views.userApi),
    path('user/<int:id>/',views.userApi),
    path('prometheus-targets/', views.syncPrometheus),
]