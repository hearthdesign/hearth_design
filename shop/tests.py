from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import (
    Print,
    Theme,
    models,
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

        self.assertEqual(print_obj.title, "Forest Path")

        self.assertEqual(print_obj.stock, 5)

        self.assertTrue(print_obj.in_stock)


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

        self.print_obj.themes.add(self.theme)

    def test_theme_filter_page_loads(self):

        response = self.client.get(
            reverse("theme_filter"),
            {"theme": "nature"},
        )

        self.assertEqual(response.status_code, 200)

    def test_theme_filter_returns_print(self):

        response = self.client.get(
            reverse("theme_filter"),
            {"theme": "nature"},
        )

        self.assertContains(response, "Forest")


# ======================================================
# Homepage Test
# ======================================================


class HomepageTest(TestCase):
    def test_homepage_loads(self):

        response = self.client.get(reverse("homepage"))

        self.assertEqual(response.status_code, 200)



