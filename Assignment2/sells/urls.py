from django.urls import path
from .views import SellHeaderView, SellHeaderDetailView, SellDetailView

urlpatterns = [
    # Sell Header
    path('sell/', SellHeaderView.as_view(), name='sell-list'),
    path('sell/<str:code>/', SellHeaderDetailView.as_view(), name='sell-detail'),

    # Sell Detail
    path('sell/<str:header_code>/details/', SellDetailView.as_view(), name='sell-details'),
]