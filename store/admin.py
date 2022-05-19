from django.contrib import admin
from . models import Product, ProductOffer, CategoryOffer
from django.utils.html import mark_safe




class ProductAdmin(admin.ModelAdmin):
    #auto update slug from category name
    prepopulated_fields = {'slug': ('product_name',)}
    # display fields in list in admin side
    list_display        = ( 'product_name', 'price', 'category', 'stock', 'modified_date', 'is_available', 'is_trending')
    # can edit the field in admin side
    list_editable        = ('is_available', 'is_trending',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOffer )
admin.site.register( CategoryOffer)