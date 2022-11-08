from django.db import models
from django_countries.fields import CountryField
from src.core.choices import TYPE_OF_PRODUCT


# class Country(models.Model):
#     country = CountryField()
#
#     def __str__(self):
#         return self.country.name
#
#
# class City(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     city = models.CharField(max_length=200)
#
#     def __str__(self):
#         return f"{self.city}, {self.country}"


class CommonPart(models.Model):
    create_data = models.DateField(auto_now_add=True)
    update_data = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# class Product(CommonPart):
#     name = models.CharField(max_length=25, choices=TYPE_OF_PRODUCT)
#     model = models.CharField(max_length=10)
#     presentation_data = models.DateField()
#
#     def __str__(self):
#         return f"{self.name}, {self.model}"
