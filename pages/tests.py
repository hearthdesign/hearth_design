# pages/tests.py
from django.test import TestCase


class SEOFilesTestCase(TestCase):
    def test_robots_txt_returns_200(self):
        """Test that robots.txt is accessible and returns HTTP 200"""
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        # Verify it's served as plain text
        self.assertIn("text/plain", response["Content-Type"])

    def test_sitemap_xml_returns_200(self):
        """Test that sitemap.xml is accessible and returns HTTP 200"""
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        # Verify it's served as XML
        self.assertIn("xml", response["Content-Type"])
