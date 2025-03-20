# purchases/urls.py
from django.urls import path
from .views import PurchaseHeaderView, PurchaseHeaderDetailView, PurchaseDetailView

urlpatterns = [
    # Purchase Header
    path('purchase/', PurchaseHeaderView.as_view(), name='purchase-list'),
    path('purchase/<str:code>/', PurchaseHeaderDetailView.as_view(), name='purchase-detail'),

    # Purchase Detail
    path('purchase/<str:header_code>/details/', PurchaseDetailView.as_view(), name='purchase-details'),
]