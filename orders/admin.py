from django.contrib import admin

from .models import OrderItem, Order


class OrderItemTabulareAmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "name", "price", "quntity"
    search_fields = ("product", "name")
    extra = 0


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp"
    )

    search_fields = (
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "name", "quantity",)
    search_fields = ("order", "product", "name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp"
    )
    search_fields = (
        "id",
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "created_timestamp"
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "created_timestamp"
    )
    inlines = (OrderItemTabulareAmin,)

