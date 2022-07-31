import graphene
from django.db.models import F

from orders.base import CreateOrderPayload, OrderMutationSuccess, OrderMutationFail
from orders.models import Order, CartItem
from products.models import Product


CART_ADD = 'ADD'
CART_DECREASE = 'DECREASE'
CART_REMOVE = 'REMOVE'

CART_ACTIONS = (
    (CART_ADD, 'ADD'),
    (CART_DECREASE, 'DECREASE'),
    (CART_REMOVE, 'REMOVE')
)


def create_or_increment_cart_item(order: Order, product: Product):
    cart_item, created = CartItem.objects.get_or_create(order=order, product=product)
    if not created:
        cart_item.quantity = F('quantity') + 1
        cart_item.save()
    return


def delete_cart_item(order: Order, product: Product):
    CartItem.objects.filter(order=order, product=product).delete()
    return


def decrement_cart_item(order: Order, product: Product):
    if CartItem.objects.filter(order=order, product=product).exists():
        cart_item = CartItem.objects.get(order=order, product=product)
        cart_item.quantity = F('quantity') - 1
        cart_item.save()

        # we get the new value
        cart_item.refresh_from_db()

        # if cart item quantity == 0, we delete it
        if cart_item.quantity == 0:
            cart_item.delete()
    return


class CartMutation(graphene.Mutation):
    """
    We use this mutation to add items to cart, incrementing,
    decrementing cart item quantity and deleting cart item.

    :param product_id: Id of an existing product \n
    :param action: valid choices are 'ADD', 'DECREASE' and 'REMOVE' \n\n

    ADD: Adds item to cart or increments cart quantity by 1 \n
    DECREASE: Decreases cart item quantity by 1, if new quantity
    is zero, the cart item is deleted \n
    REMOVE: Deletes the cart item
    """
    class Arguments:
        product_id = graphene.Int()
        action = graphene.String(description=f"Choices are: {CART_ADD}, "
                                             f"{CART_DECREASE} or {CART_REMOVE}")

    Output = CreateOrderPayload

    @classmethod
    def mutate(cls, root, info, product_id, action):
        user = info.context.user
        if user.is_authenticated:
            # if the product exists we update the order item
            if Product.objects.filter(id=product_id).exists():
                product = Product.objects.get(id=product_id)
                order, created = Order.objects.get_or_create(complete=False, user=user)
                # we perform appropriate add, increment, decrement and delete
                if action == CART_ADD:
                    create_or_increment_cart_item(order=order, product=product)
                elif action == CART_DECREASE:
                    decrement_cart_item(order=order, product=product)
                elif action == CART_REMOVE:
                    delete_cart_item(order=order, product=product)
                else:
                    return OrderMutationFail(
                        error_message=f"Invalid cart action, "
                                      f"valid actions are: {CART_ADD}, {CART_DECREASE} or {CART_REMOVE}")
                return OrderMutationSuccess(order=order)
            else:
                OrderMutationFail(error_message="Invalid product id")
        # We can handle the guest add to cart
        # logic here in an else block but for now
        # we make it for logged-in users only
        return OrderMutationFail(error_message="Please login to add to cart")


class Mutation(graphene.ObjectType):
    update_cart = CartMutation.Field()
