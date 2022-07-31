import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from .types import OrderType


class OrderQuery(graphene.ObjectType):
    cart = relay.Node.Field(OrderType)
    order_history = DjangoFilterConnectionField(OrderType)

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        if info.context.user.is_authenticated:
            user = info.context.user
            return queryset.filter(complete=False, user=user).first()
        return queryset.none()
