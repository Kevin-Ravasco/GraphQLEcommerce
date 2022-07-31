import graphene

from accounts.schema import Mutation as AccountsMutation, Query as AccountsQuery
from orders.schema import OrdersQuery, OrderMutation
from products.schema import ProductsQuery, ProductsMutation


class Query(AccountsQuery, ProductsQuery, OrdersQuery, graphene.ObjectType):
    pass


class Mutation(AccountsMutation, ProductsMutation, OrderMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
