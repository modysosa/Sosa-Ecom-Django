from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models on the admin

admin.site.register(ShippingAddress)

admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
# Extend our Order Model

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name","email","shipping_address","amount_paid","date_ordered","shipped","date_shipped"]
    inlines = [OrderItemInline,]

# unregister order model

admin.site.unregister(Order)

# Register our Order Model with the OrderAdmin
admin.site.register(Order, OrderAdmin)