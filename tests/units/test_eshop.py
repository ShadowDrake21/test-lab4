import unittest
from tests.eshop import Product, ShoppingCart, Order
from unittest.mock import MagicMock

class TestEshop(unittest.TestCase):
    def setUp(self):
        self.product = Product(name = 'Test', price=100.0, available_amount=10)
        self.cart = ShoppingCart()

    def tearDown(self):
        self.cart.remove_product(self.product)

    # Tests for product entity
    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test")
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.available_amount, 10)

    def test_product_availability(self):
        self.assertTrue(self.product.is_available(5))
        self.assertFalse(self.product.is_available(15))

    def test_product_buy(self):
        self.product.buy(3)
        self.assertEqual(self.product.available_amount, 7)
        with self.assertRaises(ValueError):
            self.product.buy(8)

    def test_product_equality(self):
        same_product = Product(name="Test", price=100.0, available_amount=5)
        different_product = Product(name="Other test", price=200.0, available_amount=5)
        self.assertEqual(self.product, same_product)
        self.assertNotEqual(self.product, different_product)

    def test_product_hash(self):
        same_product = Product(name="Test", price=100.0, available_amount=5)
        different_product = Product(name="Other test", price=200.0, available_amount=5)

        self.assertEqual(hash(self.product), hash(same_product))
        self.assertNotEqual(hash(self.product), hash(different_product))

    # Tests for shopping cart entity
    def test_modify_product_quantity(self):
        self.cart.add_product(self.product, 2)
        self.cart.update_product_quantity(self.product, 5)
        self.assertEqual(self.cart.products[self.product],5)
        self.cart.update_product_quantity(self.product, 0)
        self.assertNotIn(self.product, self.cart.products)

    def test_add_and_remove_product(self):
        self.cart.add_product(self.product, 2)
        self.assertTrue(self.cart.contains_product(self.product))
        self.cart.remove_product(self.product)
        self.assertNotIn(self.product, self.cart.products)

    def test_calculate_total_correctly(self):
        self.cart.add_product(self.product, 2)
        self.assertEqual(self.cart.calculate_total(), 200.0)


    # Tests for order entity
    def test_cart_order_submit(self):
        self.cart.submit_cart_order = MagicMock()
        order = Order(self
                      .cart)
        order.place_order()
        self.cart.submit_cart_order.assert_called_once()

    def test_order_placement(self):
        self.cart.add_product(self.product, 3)
        order = Order(self.cart)
        order.place_order()
        self.assertEqual(self.product.available_amount, 7)
        self.assertEqual(len(self.cart.products), 0)