# pages/views.py
from django.views.generic import TemplateView


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"


class SitemapXmlView(TemplateView):
    template_name = "sitemap.xml"
    content_type = "application/xml"
