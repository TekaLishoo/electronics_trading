from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django_countries.fields import CountryField
from src.core.models import CommonPart
from src.core.choices import TYPE_OF_OBJECT, TYPE_OF_PRODUCT
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField


class Country(models.Model):
    country = CountryField()

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.city}, {self.country}"

    class Meta:
        verbose_name_plural = "Cities"


class Product(CommonPart):
    name = models.CharField(max_length=25, choices=TYPE_OF_PRODUCT)
    model = models.CharField(max_length=10)
    presentation_data = models.DateField()

    def __str__(self):
        return f"{self.name}, {self.model}"


class NetworkObject(CommonPart):
    """
    Model presents an object in electronics trading network.
    """

    type = models.PositiveIntegerField(choices=TYPE_OF_OBJECT)
    name = models.CharField(max_length=50)
    mail = models.EmailField()
    location_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    location_city = ChainedForeignKey(
        City,
        chained_field="location_country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True,
        sort=True,
    )
    location_street = models.CharField(max_length=250)
    location_house = models.PositiveIntegerField()
    supplier = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    debt = MoneyField(decimal_places=2, max_digits=8, default_currency="BYN")

    def save(self, *args, **kwargs):
        """
        Checking the right order of objects in network.
        """

        if self.supplier is None:
            super(NetworkObject, self).save(*args, **kwargs)
        elif self.type > self.supplier.type:
            super(NetworkObject, self).save(*args, **kwargs)
        else:
            raise ValueError(
                "Invalid supplier: please, keep the right order of suppliers."
            )

    def __str__(self):
        return (
            f"{self.type}: {self.name}, {self.location_city}. Debt: {self.debt.amount}"
        )


class PresentProducts(models.Model):
    """
    Model defines which products are presented
    in a particular object of trading network.
    """

    object = models.ForeignKey(NetworkObject, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f'{self.object.name}: {", ".join(self.products.all().values_list("name", flat=True))}'

    class Meta:
        verbose_name_plural = "Present Products"


class ObjectEmployees(models.Model):
    """
    Model defines a list of employees for
    a particular object of trading network.
    """

    object = models.ForeignKey(NetworkObject, on_delete=models.CASCADE)
    employees = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.object.name}: {", ".join(self.employees.all().values_list("last_name", flat=True))}'

    class Meta:
        verbose_name_plural = "Object Employees"
