Feature:Shopping cart
  We want to test that shopping cart functionality works correctly
  Scenario: Successful add product to cart
    Given The product has availability of 123
    And An empty shopping cart
    When I add product to the cart in amount 123
    Then Product is added to the cart successfully
  Scenario: Failed add product to cart
    Given The product has availability of 123
    And An empty shopping cart
    When I add product to the cart in amount 124
    Then Product is not added to cart successfully
  Scenario: Adding a product to an empty shopping cart
    Given A product with name MacBook 16, price 40000.0, and availability 14
    And An empty shopping cart
    When I add product to the cart in amount 5
    Then The cart should contain the product with the correct amount
  Scenario: Removing a product from the shopping cart
    Given A product with name MacBook 16, price 40000.0, and availability 14
    And A shopping cart with the product added
    When I remove the product from the cart
    Then The cart should be empty
  Scenario: Updating the quantity of a product in the cart
    Given A product with name MacBook 16, price 40000.0, and availability 14
    And A shopping cart with the product added in amount 4
    When I update the quantity of the product in the cart to 2
    Then The cart should contain the product with the updated amount 2