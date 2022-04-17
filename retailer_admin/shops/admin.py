from django.contrib import admin

from shops.models import ShopsModel


@admin.register(ShopsModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "city", "street", "house", "floor")
