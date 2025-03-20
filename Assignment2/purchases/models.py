# purchases/models.py
from django.db import models
from items.models import Item
from stock_warehouse.base_models import BaseModel

class PurchaseHeader(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class PurchaseDetail(models.Model):
    item_code = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='purchase_details')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    header_code = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name='details')

    def __str__(self):
        return f"{self.item_code.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        # Update stock dan balance item saat membuat atau mengubah detail pembelian
        super().save(*args, **kwargs)
        self.item_code.stock += self.quantity
        self.item_code.balance += self.quantity * self.unit_price
        self.item_code.save()