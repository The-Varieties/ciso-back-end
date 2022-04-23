from django.urls import path
from database import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('instance/',views.instanceApi),
    path('instance/<int:id>/',views.instanceApi),
]