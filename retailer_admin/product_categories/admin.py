from django.contrib import admin

from product_categories.models import ProductCategoryModel


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
