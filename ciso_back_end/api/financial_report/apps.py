from django.apps import AppConfig

from ciso_back_end.api import financial_report


class FinancialReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ciso_back_end.api.financial_report'
