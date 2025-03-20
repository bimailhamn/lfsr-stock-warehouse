from rest_framework import serializers
from .models import SellHeader, SellDetail

class SellDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetail
        fields = ['item_code', 'quantity', 'header_code', 'unit_price']

class SellHeaderSerializer(serializers.ModelSerializer):
    details = SellDetailSerializer(many=True, read_only=True)

    class Meta:
        model = SellHeader
        fields = ['code', 'date', 'description', 'details']