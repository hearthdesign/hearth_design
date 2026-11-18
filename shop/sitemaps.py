from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import translation


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # We define the base view names and build localized entries in location()
        base_views = [
            "homepage",
            "illustration_gallery",
            "photography_gallery",
            "contact",
            "terms_of_service",
            "privacy_policy",
        ]

        # Create a list of tuples: (view_name, language_code)
        localized_items = []
        for lang_code, _ in settings.LANGUAGES:
            for view_name in base_views:
                localized_items.append((view_name, lang_code))

        return localized_items

    def location(self, item):
        view_name, lang_code = item
        # Temporarily activate the language to reverse the correct prefixed URL
        with translation.override(lang_code):
            return reverse(view_name)
