from django.urls import path
from .views import ReportView

urlpatterns = [
    path('report/<str:item_code>/', ReportView.as_view(), name='report'),
]