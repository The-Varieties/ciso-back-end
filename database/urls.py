from django.urls import path
from database import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    path('instance/',views.instanceApi),
    path('instance/([0-9]+)/',views.instanceApi),

    path('instance/savefile/',views.SaveFile)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)