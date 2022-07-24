import graphene

from accounts.schema import Mutation as AccountsMutation, Query as AccountsQuery
from products.schema import ProductsQuery, ProductsMutation


class Query(AccountsQuery, ProductsQuery, graphene.ObjectType):
    pass


class Mutation(AccountsMutation, ProductsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
