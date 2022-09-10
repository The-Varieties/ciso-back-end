from django.urls import path
from ciso_back_end.api.users import views

urlpatterns = [
    path('users/', views.user_api),
    path('users/<int:id>/', views.user_api)
]
