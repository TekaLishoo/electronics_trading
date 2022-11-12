from django.core.management.base import BaseCommand
from src.electronics.models import Product
from src.core.choices import TYPE_OF_PRODUCT
from random import choice, randint
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Create a given number of random products"

    def add_arguments(self, parser):
        parser.add_argument("amount", nargs="+", type=int)

    def handle(self, *args, **options):
        for n in range(*options["amount"]):
            product = Product()

            product.name = choice(TYPE_OF_PRODUCT)[0]
            product.model = (
                f'{chr(randint(ord("A"), ord("Z")))}{choice(range(100, 900))}'
            )
            product.presentation_data = date.today() + timedelta(days=randint(1, 20))

            product.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created %s products" % int(*options["amount"])
            )
        )
