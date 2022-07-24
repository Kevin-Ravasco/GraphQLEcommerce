import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from products.models import Product
from products.types import CategoryType, ProductType


class CategoryQuery(graphene.ObjectType):
    category = relay.Node.Field(CategoryType)
    all_categories = DjangoFilterConnectionField(CategoryType)


class ProductQuery(graphene.ObjectType):
    product = relay.Node.Field(ProductType)
    all_products = DjangoFilterConnectionField(ProductType, description="Get the list of all products")

    def resolve_all_products(self, info, **kwargs):
        queryset = Product.objects.select_related('category').all()
        return queryset

