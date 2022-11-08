from django.contrib import admin
from src.electronics.models import (
    Country,
    City,
    Product,
    NetworkObject,
    PresentProducts,
    ObjectEmployees,
)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Product)
admin.site.register(NetworkObject)
admin.site.register(PresentProducts)
admin.site.register(ObjectEmployees)
