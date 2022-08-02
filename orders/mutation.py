import graphene
from django.db.models import F

from orders.base import OrderPayload, OrderMutationSuccess, OrderMutationFail
from orders.models import Order, CartItem, ShippingInformation
from orders.types import ShippingInformationType
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

    Output = OrderPayload

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


class ShippingInformationMutation(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int()
        town = graphene.String()
        address = graphene.String()
        further_description = graphene.String()

    shipping_information = graphene.Field(ShippingInformationType)

    @classmethod
    def mutate(cls, root, info, order_id, town, address, further_description):
        user = info.context.user
        if user.is_authenticated:
            if Order.objects.filter(id=order_id).exists():
                order = Order.objects.get(id=order_id)
                shipping_information = ShippingInformation.objects.create(user=user, order=order,
                                                                          town=town, address=address,
                                                                          further_description=further_description)
                return ShippingInformationMutation(shipping_information=shipping_information)

            # we can handle guest user checkout
            return OrderMutationFail(error_message="Invalid order ID")
        # we can handle guest user checkout
        return OrderMutationFail(error_message="Please login to add to checkout")


class CheckoutMutation(graphene.Mutation):
    """
    This mutation is used to handle the checkout process.
    The user has to have items in cart already in order
    to complete the checkout process.
    """

    Output = OrderPayload

    @classmethod
    def mutate(cls, root, info):
        user = info.context.user
        if user.is_authenticated:
            if Order.objects.filter(complete=False, user=user).exists():
                # make the order complete
                order = Order.objects.get(complete=False, user=user)
                order.complete = True
                order.save()
                return OrderMutationSuccess(order=order)
            else:
                OrderMutationFail(error_message="No order with status complete=False")

        else:
            # we can handle guest user checkout
            return OrderMutationFail(error_message="Please login to add to checkout")


class Mutation(graphene.ObjectType):
    update_cart = CartMutation.Field()
    checkout = CheckoutMutation.Field()
    add_shipping_info = ShippingInformationMutation.Field()
