from django.contrib import admin

from products.models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "category",
        "photo_preview",
    )

    readonly_fields = ("photo_preview",)

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = "Photo preview"
    photo_preview.allow_tags = True
