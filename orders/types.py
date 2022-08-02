import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from .models import Order, CartItem, ShippingInformation


class OrderType(DjangoObjectType):
    pk = graphene.Int(source='pk')

    class Meta:
        model = Order
        filter_fields = ['status', 'complete', 'timestamp']
        interfaces = (relay.Node,)


class OrderItemType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class ShippingInformationType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = ShippingInformation
        fields = ['order', 'address', 'town', 'further_description']
