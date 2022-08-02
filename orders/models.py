from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product


User = get_user_model()

ORDER_PENDING = 'PENDING'
ORDER_OUT_FOR_DELIVERY = 'OUT FOR DELIVERY'
ORDER_DELIVERED = 'DELIVERED'

ORDER_STATUS = (
    (ORDER_PENDING, 'Pending'),
    (ORDER_OUT_FOR_DELIVERY, 'Out for Delivery'),
    (ORDER_DELIVERED, 'Delivered')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=17, choices=ORDER_STATUS, default=ORDER_PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_total(self):
        order_items = CartItem.objects.filter(order=self)
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = CartItem.objects.filter(order=self)
        total = sum([item.quantity for item in order_items])
        return total


class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_information')
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    further_description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
