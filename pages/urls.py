# pages/urls.py
from django.urls import path

from .views import RobotsTxtView, SitemapXmlView

urlpatterns = [
    path("robots.txt", RobotsTxtView.as_view(content_type="text/plain"), name="robots"),
    path(
        "sitemap.xml",
        SitemapXmlView.as_view(content_type="application/xml"),
        name="sitemap",
    ),
]
