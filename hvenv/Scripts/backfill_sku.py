import os
import django

# Point to your settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hearth_shop.settings")
django.setup()

from shop.models import Print

for i, p in enumerate(Print.objects.all(), start=1):
    if not p.sku:
        p.sku = f"{p.type[:3].upper()}-{i}"
        p.save()

print("Backfill complete.")