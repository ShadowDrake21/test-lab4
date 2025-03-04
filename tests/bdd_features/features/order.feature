Feature: Order
  As a user, I want to place orders with products in my shopping cart and ensure the order is processed correctly,
  so I can complete my purchases and update product availability.
Scenario: Placing an order with a valid cart
  Given A product with name MacBook 16, price 40000.0, and availability 14
  And A shopping cart with the product added in amount 3
  When I place an order with the cart
  Then The order should be placed successfully and the product availability should be updated
