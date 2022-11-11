from django.core.management.base import BaseCommand
from src.electronics.models import NetworkObject, Country, City, PresentProducts, Product
from src.core.choices import TYPE_OF_OBJECT
from random import choice, randint
from faker import Faker


class Command(BaseCommand):
    help = "Create a given number of random network objects."

    def add_arguments(self, parser):
        parser.add_argument("amount", nargs="+", type=int)

    def handle(self, *args, **options):
        countries = list(Country.objects.all())

        for n in range(*options["amount"]):
            object = NetworkObject()

            object.type = choice(TYPE_OF_OBJECT)[0]
            name = Faker().word().capitalize()
            while len(name) >= 100:
                name = Faker().word().capitalize()
            object.name = name
            object.mail = f'{name}@mail.ru'
            country = choice(countries)
            city = list(City.objects.filter(country=country))
            object.location_country = country
            object.location_city = choice(city)
            object.location_street = Faker().word().capitalize()
            object.location_house = randint(1, 100)
            if object.type != 0:
                supplier = list(NetworkObject.objects.filter(type__lt=object.type))
                object.supplier = choice(supplier)
            object.debt = choice(range(10, 1000))

            object.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created %s objects of network" % int(*options["amount"])
            )
        )
