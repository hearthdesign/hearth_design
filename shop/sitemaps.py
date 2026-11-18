from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # List all the main named URL routes on your site
        return [
            "homepage",
            "illustration_gallery",
            "photography_gallery",
            "contact",
            "terms_of_service",
            "privacy_policy",
        ]

    def location(self, item):
        return reverse(item)
