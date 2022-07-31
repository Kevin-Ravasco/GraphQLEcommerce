from graphene import relay
from graphene_django import DjangoObjectType

from products.models import Category, Product, ProductMedia


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'products']
        interfaces = (relay.Node,)


class ProductMediaType(DjangoObjectType):
    class Meta:
        model = ProductMedia
        fields = ['product', 'image']

    def resolve_image(self, info):
        # to return image url instead of name
        # info.context.build_absolute_uri(self.image.url)
        return self.image.url


class ProductType(DjangoObjectType):
    """
    Defining the fields for our Product that are available.

    We are able to search product using the following fields:
    as name, slug, description, category, category name and
    category slug
    """
    class Meta:
        model = Product
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'slug': ['exact'],
            'description': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
            'category__slug': ['exact'],
        }
        interfaces = (relay.Node,)
