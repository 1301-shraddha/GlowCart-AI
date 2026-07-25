from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "skin_type",
        "skin_concern",
        "category_type",
        "stock",
    )


admin.site.register(Category)