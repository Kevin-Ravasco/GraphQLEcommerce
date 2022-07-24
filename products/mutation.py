import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from products.forms import CategoryForm, ProductForm, ProductMediaForm
from products.types import CategoryType, ProductType, ProductMediaType


class CategoryMutation(DjangoModelFormMutation):
    category = graphene.Field(CategoryType)

    class Meta:
        form_class = CategoryForm
        input_field_name = 'data'
        return_field_name = 'category'


class ProductMutation(DjangoModelFormMutation):
    product = graphene.Field(ProductType)

    class Meta:
        form_class = ProductForm
        input_field_name = 'data'
        return_field_name = 'product'


class ProductMediaMutation(DjangoModelFormMutation):
    product_media = graphene.Field(ProductMediaType)

    class Meta:
        form_class = ProductMediaForm
        input_field_name = 'data'
        return_field_name = 'product_media'


class Mutation(graphene.ObjectType):
    create_category = CategoryMutation.Field()
    create_product = ProductMutation.Field()
