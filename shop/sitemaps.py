from django.contrib.sitemaps import Sitemap
from .models import Print


class PrintSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Print.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.date