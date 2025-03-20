from django.db import models
from stock_warehouse.base_models import BaseModel

class Item(BaseModel):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name