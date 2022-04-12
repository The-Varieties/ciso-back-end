from django.urls import path
from database import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    path(r'<instance>',views.instanceApi),
    path(r'<instance/([0-9]+)>',views.instanceApi),

    path(r'<instance/savefile>',views.SaveFile)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)