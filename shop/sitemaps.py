from django.contrib.sitemaps import Sitemap


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Return root-relative paths for your main pages (Django i18n middleware will prefix them automatically if configured, or you can supply them directly)
        return [
            "/",
            "/gallery/illustrations/",
            "/gallery/photography/",
            "/contact/",
            "/terms/",
            "/privacy-policy/",
        ]

    def location(self, item):
        return item
