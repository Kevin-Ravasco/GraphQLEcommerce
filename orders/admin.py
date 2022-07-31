from django.contrib import admin

from .models import Order, ShippingInformation, CartItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'complete', 'timestamp']
    list_filter = ['status']


@admin.register(ShippingInformation)
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ['address', 'town', 'timestamp']

# admin.site.register(CartItem)
