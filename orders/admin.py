from django.contrib import admin
from . models import Payment, Order, OrderProduct
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('user', 'payment', 'product', 'quantity', )

class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['order_number', 'full_name',  'email', 'order_total', 'status', 'tax','is_ordered']
    list_filter = ['status', 'is_ordered']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)