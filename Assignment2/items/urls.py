from django.urls import path
from .views import ItemListCreateView, ItemDetailView

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<str:code>/', ItemDetailView.as_view(), name='item-detail'),
]