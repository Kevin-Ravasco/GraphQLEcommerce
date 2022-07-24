from products.mutation import Mutation
from products.queries import CategoryQuery, ProductQuery


class ProductsQuery(CategoryQuery, ProductQuery):
    pass


class ProductsMutation(Mutation):
    pass
