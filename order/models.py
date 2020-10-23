from django.db.models import Sum
from django.db import models


class Order(models.Model):
    number = models.IntegerField()
    create_date = models.DateTimeField()

    # @property
    # def price(self):
    #     return self.orderitem_set.all().aggregate(
    #         price=Sum('product_price')).get('price')

    def __str__(self):
        return str(self.number)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.IntegerField()

    def __str__(self):
        return self.product_name