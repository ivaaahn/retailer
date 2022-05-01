from django.contrib import admin

from products.models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "category",
    )
