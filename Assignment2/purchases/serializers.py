# purchases/serializers.py
from rest_framework import serializers
from .models import PurchaseHeader, PurchaseDetail

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = ['item_code', 'quantity', 'unit_price', 'header_code']

class PurchaseHeaderSerializer(serializers.ModelSerializer):
    details = PurchaseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseHeader
        fields = ['code', 'date', 'description', 'details']