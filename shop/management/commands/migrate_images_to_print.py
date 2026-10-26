# your_app/management/commands/import_prints_from_media.py
import os
from datetime import date
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Print
from django.conf import settings # Import settings to access MEDIA_ROOT

class Command(BaseCommand):
    help = 'Bulk-import images from media/prints/YYYY/MMDD/ into Print model'

    def add_arguments(self, parser):
        parser.add_argument('--type', type=str, choices=['illustration', 'photo'], default='illustration')

    def handle(self, *args, **kwargs):
        type = kwargs['type']
        today = date.today()
        year = today.strftime('%Y')
        month_day = today.strftime('%m%d')
        date_path = f"{year}/{month_day}"
        media_dir = os.path.join(settings.MEDIA_ROOT, 'prints', year, month_day)
        if not os.path.exists(media_dir):
            self.stdout.write(self.style.WARNING(f"No folder found: {media_dir}"))
            return

        imported = 0
        skipped = 0

        for filename in os.listdir(media_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = f'prints/{date_path}/{filename}'
                if Print.objects.filter(image=image_path).exists():
                    skipped += 1
                    continue

                title = os.path.splitext(filename)[0]
                Print.objects.create(
                    title=title,
                    slug=slugify(title),
                    type=type,
                    date=today,
                    image=image_path,
                    in_stock=True
                )
                imported += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {imported} prints. Skipped {skipped} duplicates."))
