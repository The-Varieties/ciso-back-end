from django.urls import path
from login import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('login/',views.loginApi),
    path('login/<int:id>/',views.loginApi),
    path('prometheus-targets/', views.syncPrometheus2),
]