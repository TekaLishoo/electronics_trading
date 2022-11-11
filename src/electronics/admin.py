from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

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


@admin.action(description="Clear debt")
async def clear_debt(modeladmin, request, queryset):
    if queryset.count() <= 20:
        queryset.update(debt=0)
    else:
        async for obj in queryset:
            obj.debt.amount = 0


class PresentProductsInline(admin.StackedInline):
    model = PresentProducts


class ObjectEmployeesInline(admin.StackedInline):
    model = ObjectEmployees


@admin.register(NetworkObject)
class NetworkObjectAdmin(admin.ModelAdmin):
    inlines = [PresentProductsInline, ObjectEmployeesInline]
    list_display = [
        "type",
        "name",
        "location_city",
        "debt",
        "get_supplier",
    ]
    list_filter = [
        "location_city",
    ]
    list_display_links = [
        "get_supplier",
    ]
    list_select_related = True
    actions = [
        clear_debt,
    ]

    def get_supplier(self, obj):
        if obj.supplier is None:
            return "No supplier"
        else:
            url = reverse(
                "admin:electronics_networkobject_change", args=(obj.supplier.id,)
            )
            return mark_safe("<a href='%s'>'%s'</a>" % (url, obj.supplier.name))

    get_supplier.allow_tags = True
    get_supplier.short_description = "Supplier"
