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
admin.site.register(PresentProducts)
admin.site.register(ObjectEmployees)


class PresentProductsInline(admin.StackedInline):
    model = PresentProducts


class ObjectEmployeesInline(admin.StackedInline):
    model = ObjectEmployees


@admin.register(NetworkObject)
class NetworkObjectAdmin(admin.ModelAdmin):
    inlines = [PresentProductsInline, ObjectEmployeesInline]

