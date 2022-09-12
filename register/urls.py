from django.urls import path
from register import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('register/',views.registerApi),
    path('register/<int:id>/',views.registerApi),
    path('prometheus-targets/', views.syncPrometheus2),
]