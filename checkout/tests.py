
from decimal import Decimal
from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model
from checkout.services.webhooks import handle_checkout_session
from checkout.views import fulfill_order_from_stripe_session
from shop.models import Print
from .models import (
    Cart,
    CartItem,
    Order,
    OrderItem,
)

User = get_user_model()

# ======================================================
# Cart Tests
# ======================================================

class CartTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="tester",
            password="password123",
        )

        self.print_obj = Print.objects.create(
            title="Mountain",
            type="photo",
            stock=10,
            price=Decimal("50.00"),
        )

    def test_cart_creation(self):

        cart = Cart.objects.create(user=self.user)

        self.assertEqual(cart.user, self.user)

    def test_cart_item_creation(self):

        cart = Cart.objects.create(user=self.user)

        item = CartItem.objects.create(
            cart=cart,
            print=self.print_obj,
            quantity=2,
            price_at_time=self.print_obj.price,
        )

        self.assertEqual(item.quantity, 2)

    def test_cartitem_string_representation(self):

        cart = Cart.objects.create(user=self.user)

        item = CartItem.objects.create(
            cart=cart,
            print=self.print_obj,
            quantity=2,
            price_at_time=self.print_obj.price,
        )

        self.assertIn(self.print_obj.title, str(item))


# ======================================================
# Order Tests
# ======================================================


class OrderTest(TestCase):
    def setUp(self):

        self.print_obj = Print.objects.create(
            title="Ocean",
            type="photo",
            stock=3,
            price=Decimal("35.00"),
        )

    def test_order_creation(self):

        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            total_price=Decimal("35.00"),
        )

        self.assertIsNotNone(order.id)

    def test_order_starts_unpaid(self):

        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
        )

        self.assertFalse(order.is_paid)

    def test_order_item_creation(self):

        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
        )

        item = OrderItem.objects.create(
            order=order,
            print=self.print_obj,
            quantity=1,
            price=self.print_obj.price,
        )

        self.assertEqual(item.quantity, 1)

    # ======================================================
    # Duplicate order prevention Test
    # ======================================================

    def test_order_session_id_must_be_unique(self):

        Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            stripe_session_id="cs_test_123",
        )

        with self.assertRaises(IntegrityError):
            Order.objects.create(
                customer_name="John Doe",
                customer_email="john@example.com",
                stripe_session_id="cs_test_123",
            )


# ======================================================
# Authentication Tests
# ======================================================


class AuthenticationTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="tester",
            password="password123",
        )

    def test_cart_requires_login(self):

        response = self.client.get(reverse("cart_view"))

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_access_cart(self):

        self.client.login(
            username="tester",
            password="password123",
        )

        response = self.client.get(reverse("cart_view"))

        self.assertEqual(response.status_code, 200)

# ======================================================
# Checkout and Webhook Tests
# ======================================================


class CheckoutTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="tester",
            password="password123",
        )

        self.print_obj = Print.objects.create(
            title="Ocean",
            type="photo",
            stock=5,
            price=Decimal("35.00"),
        )

        self.cart = Cart.objects.create(user=self.user)

        CartItem.objects.create(
            cart=self.cart,
            print=self.print_obj,
            quantity=2,
            price_at_time=self.print_obj.price,
        )

    # ======================================================
    # Webhook Order Creation Tests
    # ======================================================

    def test_webhook_creates_order(self):

        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123",
        )

        cart = Cart.objects.create(user=user)

        CartItem.objects.create(
            cart=cart,
            print=self.print_obj,
            quantity=2,
            price_at_time=self.print_obj.price,
        )

        session = {
            "id": "cs_test_123",
            "client_reference_id": user.id,
        }

        handle_checkout_session(session)

        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()

        self.assertEqual(order.total_price, Decimal("70.00"))

        self.assertTrue(order.is_paid)

        self.assertEqual(order.customer_name, "john")

    # ======================================================
    # Webhook does not create duplicate Orders Test
    # ======================================================

    def test_webhook_does_not_create_duplicate_orders(self):

        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123",
        )

        cart = Cart.objects.create(user=user)

        CartItem.objects.create(
            cart=cart,
            print=self.print_obj,
            quantity=1,
            price_at_time=self.print_obj.price,
        )

        session = {
            "id": "cs_test_duplicate",
            "client_reference_id": user.id,
        }

        handle_checkout_session(session)

        handle_checkout_session(session)

        self.assertEqual(Order.objects.count(), 1)

    # ======================================================
    # Cart is cleared after Checkout Test
    # ======================================================

    def test_cart_is_cleared_after_checkout(self):

        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123",
        )

        cart = Cart.objects.create(user=user)

        CartItem.objects.create(
            cart=cart,
            print=self.print_obj,
            quantity=1,
            price_at_time=self.print_obj.price,
        )

        session = {
            "id": "cs_test_clear",
            "client_reference_id": user.id,
        }

        handle_checkout_session(session)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(cart.cartitem_set.count(), 0)

    # ======================================================
    # Paid Order Creation Tests
    # ======================================================

    def test_webhook_creates_paid_order(self):

        session = {
            "id": "cs_test_paid",
            "client_reference_id": self.user.id,
        }

        handle_checkout_session(session)

        order = Order.objects.get(stripe_session_id="cs_test_paid")

        self.assertTrue(order.is_paid)

    # ======================================================
    #           Order Total CALCULATION Test
    # ======================================================

    def test_order_total_calculation(self):

        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
        )

        OrderItem.objects.create(
            order=order,
            print=self.print_obj,
            quantity=2,
            price=Decimal("35.00"),
        )

        self.assertEqual(order.calculate_total(), Decimal("70.00"))

    # ======================================================
    #           Order Total Consistency Tests
    # ======================================================

    def test_order_has_correct_total(self):

        order = Order.objects.create(
            customer_name="John",
            customer_email="john@example.com",
            total_price=Decimal("70.00"),
        )

        OrderItem.objects.create(
            order=order, print=self.print_obj, quantity=2, price=Decimal("35.00")
        )

        self.assertEqual(order.total_price, Decimal("70.00"))


# ======================================================
#           Order Total Consistency Tests
# ======================================================


class CheckoutCartClearingAndStockTest(TestCase):
    def setUp(self):
        # 1. Create a test user
        self.user = User.objects.create_user(
            username="testbuyer", email="buyer@example.com", password="password123"
        )

        # 2. Create a test product with initial stock
        self.print_item = Print.objects.create(
            title="Sunset Painting", price=Decimal("50.00"), stock=10
        )

        # 3. Add item to user's cart
        self.cart, _ = Cart.objects.get_or_create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            print=self.print_item,
            quantity=2,
            price_at_time=self.print_item.price,
        )

        # 4. Create a mock Order linked to a Stripe session ID
        self.stripe_session_id = "cs_test_mocksession123"
        self.order = Order.objects.create(
            customer_name="Test Buyer",
            customer_email=self.user.email,
            stripe_session_id=self.stripe_session_id,
            total_price=Decimal("100.00"),
            is_paid=False,
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            print=self.print_item,
            quantity=2,
            price=self.print_item.price,
        )


# ======================================================
#        ORDER FULLFILLMENT AND CLEAR CART
# ======================================================


    def test_fulfill_order_clears_cart_and_reduces_stock(self):
        """Test that fulfilling a Stripe session clears the cart and decrements stock."""
        # Mock Stripe session object passed to fulfillment logic
        mock_stripe_session = {
            "id": self.stripe_session_id,
            "client_reference_id": str(self.user.id),
        }

        # Run the fulfillment function (same one called by the webhook)
        fulfill_order_from_stripe_session(mock_stripe_session)

        # 1. Assert order is marked as paid
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_paid)

        # 2. Assert product stock was reduced from 10 to 8 (10 - 2 purchased)
        self.print_item.refresh_from_db()
        self.assertEqual(self.print_item.stock, 8)

        # 3. Assert the user's cart items have been cleared/deleted
        cart_item_exists = CartItem.objects.filter(cart=self.cart).exists()
        self.assertFalse(
            cart_item_exists, "Cart items should be deleted after successful payment."
        )
