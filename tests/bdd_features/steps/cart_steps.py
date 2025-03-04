from behave import given, when, then
from app.eshop import Product, ShoppingCart

#   Scenario: Successful add product to cart
@given("The product has availability of {availability}")
def create_product_for_cart(context, availability):
    context.product = Product(name="any", price=123, available_amount=int(availability))

@given('An empty shopping cart')
def empty_cart(context):
    context.cart = ShoppingCart()

@when("I add product to the cart in amount {product_amount}")
def add_product(context, product_amount):
    try:
        context.cart.add_product(context.product, int(product_amount))
        context.add_successfully = True
    except ValueError:
        context.add_successfully = False

@then("The cart should contain the product with the correct amount")
def verify_cart_length(context):
    product_in_cart = context.cart.products.get(context.product)
    if product_in_cart is not None:
        assert product_in_cart == 5

@then("Product is added to the cart successfully")
def add_successful(context):
    assert context.add_successfully == True

#   Scenario: Failed add product to cart
@then("Product is not added to cart successfully")
def add_failed(context):
    assert context.add_successfully == False

#   Scenario: Adding a product to an empty shopping cart
@given("A shopping cart with the product added")
def create_cart_with_product(context):
    context.cart = ShoppingCart()
    context.cart.add_product(context.product, 4)

#   Scenario: Removing a product from the shopping cart
@when("I remove the product from the cart")
def remove_product_from_cart(context):
    context.cart.remove_product(context.product)

@then("The cart should be empty")
def verify_empty_cart(context):
    assert len(context.cart.products) == 0

#   Scenario: Updating the quantity of a product in the cart
@given("A shopping cart with the product added in amount {amount}")
def create_cart_with_product_and_amount(context, amount):
    context.cart = ShoppingCart()
    context.cart.add_product(context.product, int(amount))

@when("I update the quantity of the product in the cart to {new_amount}")
def update_product_quantity_in_cart(context, new_amount):
    context.cart.update_product_quantity(context.product, int(new_amount))

@then("The cart should contain the product with the updated amount {new_amount}")
def verify_updated_product_quantity_in_cart(context, new_amount):
    assert context.cart.products[context.product] == int(new_amount)

