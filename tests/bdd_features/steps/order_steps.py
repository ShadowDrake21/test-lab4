from behave import when, then
from app.eshop import  Order

@when("I place an order with the cart")
def place_order_with_cart(context):
    context.order = Order(cart=context.cart)
    context.order.place_order()

@then("The order should be placed successfully and the product availability should be updated")
def verify_order_placement(context):
    assert context.product.available_amount == 11
    assert len(context.cart.products) == 0