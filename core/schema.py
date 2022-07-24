import graphene

from accounts.schema import Mutation as AccountsMutation, Query as AccountsQuery


class Query(AccountsQuery):
    pass


class Mutation(AccountsMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
