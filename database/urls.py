from django.conf.urls import url
from database import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    url(r'^instance$',views.instanceApi),
    url(r'^instance/([0-9]+)$',views.instanceApi),

    url(r'^instance/savefile',views.SaveFile)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)