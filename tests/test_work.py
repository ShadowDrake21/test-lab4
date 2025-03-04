from datetime import datetime, timezone, timedelta

import pytest

from app.eshop import ShoppingCart, Product, Order
from services import ShippingService
from services.publisher import ShippingPublisher
from services.repository import ShippingRepository


@pytest.fixture
def shipping_service():
    return ShippingService(ShippingRepository(), ShippingPublisher())

def test_create_shipping_valid(shipping_service):
    shipping_id = shipping_service.create_shipping(
        "Нова Пошта", ["prod1", "prod2"], "order_123", datetime.now(timezone.utc) + timedelta(days=1)
    )
    assert shipping_id is not None

def test_create_shipping_invalid_type(shipping_service):
    with pytest.raises(ValueError, match="Shipping type is not available"):
        shipping_service.create_shipping("FedEx", ["prod1"], "order_123", datetime.now(timezone.utc) + timedelta(days=1))

def test_create_shipping_invalid_due_date(shipping_service):
    with pytest.raises(ValueError, match="Shipping due datetime must be greater than datetime now"):
        shipping_service.create_shipping("Нова Пошта", ["prod1"], "order_123", datetime.now(timezone.utc) - timedelta(days=1))

def test_shipping_saved_in_repository(shipping_service):
    shipping_id = shipping_service.create_shipping("Нова Пошта", ["prod1"], "order_123", datetime.now(timezone.utc) + timedelta(days=1))

    shipping_details = shipping_service.repository.get_shipping(shipping_id)

    assert shipping_details is not None
    assert shipping_details["shipping_id"] == shipping_id
    assert shipping_details["order_id"] == "order_123"

def test_process_shipping(shipping_service):
    shipping_id=shipping_service.create_shipping("Нова Пошта", ["prod1"], "order_123", datetime.now(timezone.utc)+timedelta(days=1))
    result = shipping_service.process_shipping(shipping_id)
    assert result["HTTPStatusCode"] == 200

def test_multiple_shipments_for_one_order(shipping_service):
    available_types = shipping_service.list_available_shipping_type()

    assert len(available_types) >= 2, "Test requires at least 2 shipping types."

    shipping_id_1 = shipping_service.create_shipping(
        available_types[0], ["prod1"], "order_123", datetime.now(timezone.utc) + timedelta(days=1)
    )
    shipping_id_2 = shipping_service.create_shipping(
         available_types[1], ["prod2"], "order_123", datetime.now(timezone.utc) + timedelta(days=2)
    )

    assert shipping_id_1 is not None
    assert shipping_id_2 is not None
    assert shipping_id_1 != shipping_id_2

def test_complete_shipping(shipping_service):
    shipping_id=shipping_service.create_shipping("Нова Пошта", ["prod1"], "order_123", datetime.now(timezone.utc)+timedelta(days=1))
    shipping_service.process_shipping(shipping_id)
    assert shipping_service.check_status(shipping_id) == ShippingService.SHIPPING_COMPLETED

def test_check_shipping_status(shipping_service):
    shipping_id=shipping_service.create_shipping("Нова Пошта", ["prod1"], "order_123", datetime.now(timezone.utc)+timedelta(days=1))
    status = shipping_service.check_status(shipping_id)
    assert status == ShippingService.SHIPPING_IN_PROGRESS

def test_order_placement(shipping_service):
    cart = ShoppingCart()
    cart.add_product(Product(available_amount=10, name="Product1", price=100), amount=2)
    order=Order(cart, ShippingService(ShippingRepository(), ShippingPublisher()))
    shipping_id = order.place_order("Нова Пошта")
    assert  shipping_id is not None

def test_invalid_shipping_type(shipping_service):
    with pytest.raises(ValueError, match="Shipping type is not available"):
        shipping_service.create_shipping("LOLShipping", ["prod1"], "order_123", datetime.now(timezone.utc) + timedelta(days=1))