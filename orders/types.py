from graphene import relay
from graphene_django import DjangoObjectType

from .models import Order, CartItem, ShippingInformation


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filter_fields = ['status', 'complete', 'timestamp']
        interfaces = (relay.Node,)


class OrderItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class ShippingInformationType(DjangoObjectType):
    class Meta:
        model = ShippingInformation
        fields = ['address', 'town', 'further_description']
