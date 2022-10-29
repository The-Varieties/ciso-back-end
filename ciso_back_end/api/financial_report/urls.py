from django.urls import path
from . import views

urlpatterns = [
    path('all-instances/', views.get_financial_report_all, name='get_financial_report_all'),
    path('instance/<int:instance_id>', views.get_financial_report_single_instance, name='get_financial_report_single_instance'),
]