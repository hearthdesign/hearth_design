from django.core.management.base import BaseCommand
from shop.models import Photography, Illustration


class Command(BaseCommand):

    help = "Check whether Print and Photography/Illustration data match"

    def handle(self, *args, **kwargs):

        self.stdout.write("\nPHOTOGRAPHIES\n")

        for photo in Photography.objects.select_related("print"):

            print_obj = photo.print

            self.stdout.write(
                f"""
PHOTO ID: {photo.id}

Photography.title = {photo.title}
Print.title       = {print_obj.title}

Photography.price = {photo.price}
Print.price       = {print_obj.price}

Photography.image = {photo.image}
Print.image       = {print_obj.image}
"""
            )

        self.stdout.write("\nILLUSTRATIONS\n")

        for illustration in Illustration.objects.select_related("print"):

            print_obj = illustration.print

            self.stdout.write(
                f"""
ILLUSTRATION ID: {illustration.id}

Illustration.title = {illustration.title}
Print.title        = {print_obj.title}

Illustration.price = {illustration.price}
Print.price        = {print_obj.price}

Illustration.image = {illustration.image}
Print.image        = {print_obj.image}
"""
            )