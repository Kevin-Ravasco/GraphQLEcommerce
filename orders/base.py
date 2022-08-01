import graphene

from orders.types import OrderType


class OrderMutationFail(graphene.ObjectType):
    error_message = graphene.String(required=True)


class OrderMutationSuccess(graphene.ObjectType):
    order = graphene.Field(OrderType, required=True)


class OrderPayload(graphene.Union):
    class Meta:
        types = (OrderMutationFail, OrderMutationSuccess)
