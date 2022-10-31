from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/metrics/', include('ciso_back_end.api.rightsizing_recommendation.urls')),
    path('api/metrics/', include('ciso_back_end.api.data_visualization.urls')),
    path('api/dashboard/', include('ciso_back_end.api.instances.urls')),
    path('api/users/', include('ciso_back_end.api.users.urls')),
    path('api/logins/', include('ciso_back_end.api.login.urls')),
    path('api/registers/', include('ciso_back_end.api.register.urls')),
    path('api/resource-management/', include('ciso_back_end.api.resource_management.urls'))

]
