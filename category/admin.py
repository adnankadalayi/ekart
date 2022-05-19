from django.contrib import admin
from .models import Category
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    
    #to auto update field in slug from category_name
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display        = ('category_name','slug')

admin.site.register(Category,CategoryAdmin)
