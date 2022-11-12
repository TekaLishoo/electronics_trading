from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
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
        "id",
        "type",
        "name",
        "location_city",
        "debt",
        "get_supplier",
        'btn_copy_mail',
    ]
    list_filter = [
        "location_city",
    ]
    list_display_links = [
        "id",
        "get_supplier",
    ]
    list_select_related = True
    actions = [
        clear_debt,
    ]
    readonly_fields = ['btn_copy_mail', ]

    class Media:
        js = ("js/copy_link.js",)

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

    def btn_copy_mail(self, obj):
        return format_html('<a href="#" onclick="copy_link(\'{}\')" class="button" ''id="id_selected">Copy mail</a>',
                           str(obj.mail))

    btn_copy_mail.allow_tags = True
    btn_copy_mail.short_description = "Copy mail"
