from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import (
    Theme,
    Print,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# ======================================================
# Model Tests
# ======================================================

class ThemeModelTest(TestCase):

    def test_theme_creation(self):

        theme = Theme.objects.create(
            name="Nature",
            slug="nature",
        )

        self.assertEqual(theme.name, "Nature")
        self.assertEqual(theme.slug, "nature")


class PrintModelTest(TestCase):

    def test_print_creation(self):

        print_obj = Print.objects.create(
            title="Forest Path",
            type="photo",
            stock=5,
            price=Decimal("25.00"),
        )

        self.assertEqual(
            print_obj.title,
            "Forest Path"
        )

        self.assertEqual(
            print_obj.stock,
            5
        )

        self.assertTrue(
            print_obj.in_stock
        )


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

        cart = Cart.objects.create(
            user=self.user
        )

        self.assertEqual(
            cart.user,
            self.user
        )

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

        self.assertEqual(
            item.quantity,
            2
        )

    def test_cartitem_string_representation(self):

        cart = Cart.objects.create(
            user=self.user
        )

        item = CartItem.objects.create(
            cart=cart,
            print=self.print_obj,
            quantity=2,
            price_at_time=self.print_obj.price,
        )

        self.assertIn(
            self.print_obj.title,
            str(item)
        )


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

        self.assertFalse(
            order.is_paid
        )

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

        self.assertEqual(
            item.quantity,
            1
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

        response = self.client.get(
            reverse("cart_view")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_logged_in_user_can_access_cart(self):

        self.client.login(
            username="tester",
            password="password123",
        )

        response = self.client.get(
            reverse("cart_view")
        )

        self.assertEqual(
            response.status_code,
            200
        )


# ======================================================
# Theme Filter Tests
# ======================================================

class ThemeFilterTest(TestCase):

    def setUp(self):

        self.theme = Theme.objects.create(
            name="Nature",
            slug="nature",
        )

        self.print_obj = Print.objects.create(
            title="Forest",
            type="photo",
            stock=5,
            price=Decimal("10.00"),
        )

        self.print_obj.themes.add(
            self.theme
        )

    def test_theme_filter_page_loads(self):

        response = self.client.get(
            reverse("theme_filter"),
            {"theme": "nature"},
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_theme_filter_returns_print(self):

        response = self.client.get(
            reverse("theme_filter"),
            {"theme": "nature"},
        )

        self.assertContains(
            response,
            "Forest"
        )


# ======================================================
# Homepage Test
# ======================================================

class HomepageTest(TestCase):

    def test_homepage_loads(self):

        response = self.client.get(
            reverse("homepage")
        )

        self.assertEqual(
            response.status_code,
            200
        )