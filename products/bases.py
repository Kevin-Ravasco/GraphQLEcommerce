import graphene
from graphql_auth.bases import OutputErrorType


class Output:
    """
    A class to all public classes extend to
    padronize the output
    """

    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(OutputErrorType)
