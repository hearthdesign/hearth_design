# Hearth Shop — Automated Testing

### Automated Testing approach

Automated tests were implemented using Django's built-in testing framework.

**Command**

Tests were executed using:

```bash
python manage.py test
```

**Coverage includes:**

- Model validation
- Cart functionality
- Quantity updates
- Order creation
- Stripe webhook processing
- Duplicate order prevention
- Order total calculation
- Cart cleanup after checkout
- Access control
- Theme filtering
  
### utomated Testing Results

**Results**

- 13 tests executed
- 13 tests passed
- 0 failures
- 0 test errors
  
```text
Found 13 test(s).
Ran 13 tests

OK
```

**Note**

A Neon PostgreSQL connection remains attached to the temporary
test database during teardown, preventing automatic deletion of
test_neondb. 

This appears to be related to active local development sessions or Neon connection pooling.

This occurs after successful test execution and
does not affect test results.

---

## Example: Model Test

The following test verifies successful creation of a Theme object.

```python
class ThemeModelTest(TestCase):

    def test_theme_creation(self):

        theme = Theme.objects.create(
            name="Nature",
            slug="nature",
        )

        self.assertEqual(theme.name, "Nature")
        self.assertEqual(theme.slug, "nature")
```

---

## Example: Cart Test

The following test verifies that cart items can be created and associated with a user.

```python
def test_cart_item_creation(self):

    cart = Cart.objects.create(
        user=self.user
    )

    item = CartItem.objects.create(
        cart=cart,
        print=self.print_obj,
        quantity=2,
        price_at_time=self.print_obj.price,
    )

    self.assertEqual(item.quantity, 2)
```

---

## Example: Order Test

The following test verifies successful order creation.

```python
def test_order_creation(self):

    order = Order.objects.create(
        customer_name="John Doe",
        customer_email="john@example.com",
        total_price=Decimal("35.00"),
    )

    self.assertIsNotNone(order.id)
```

---

## Example: Stripe Webhook and Checkout Tests

Additional automated tests were implemented to validate the checkout workflow and Stripe webhook processing.

These tests verify that:

- Successful Stripe checkout creates an order
- Orders are marked as paid after checkout
- Duplicate webhook events do not create duplicate orders
- Shopping carts are cleared after successful checkout
- Order totals are calculated correctly

### Example: Webhook Creates Order

The following test verifies that a completed Stripe checkout session creates an order and corresponding order items.

### Example: Duplicate Order Prevention

The following test verifies that repeated webhook events do not generate duplicate orders.

```Python
def test_webhook_does_not_create_duplicate_orders(self):

    handle_checkout_session(session)

    handle_checkout_session(session)

    self.assertEqual(
        Order.objects.count(),
        1
    )
```

###Example: Cart Cleanup After Checkout

The following test confirms that cart contents are removed after a successful order is created.

```Python
def test_cart_is_cleared_after_checkout(self):

    handle_checkout_session(session)

    self.assertEqual(
        cart.cartitem_set.count(),
        0
    )
```

### Example: Order Total Validation

The following test verifies accurate calculation of order totals based on associated OrderItems.

```Python
def test_order_total_calculation(self):

    self.assertEqual(
        order.calculate_total(),
        Decimal("70.00")
    )
```

---

## Example: Authentication Test

The following test verifies access protection for authenticated pages.

```python
def test_cart_requires_login(self):

    response = self.client.get(
        reverse("cart_view")
    )

    self.assertEqual(
        response.status_code,
        302
    )
```

---

## Example: Theme Filter Test

The following test verifies that theme filtering returns the expected artwork.

```python
def test_theme_filter_returns_print(self):

    response = self.client.get(
        reverse("theme_filter"),
        {"theme": "nature"},
    )

    self.assertContains(
        response,
        "Forest"
    )
```