import redis
from django.conf import settings
from django.contrib import admin

from products.models import ProductModel

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
        "description",
        "category",
        "photo_preview",
    )

    readonly_fields = ("photo_preview",)

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = "Photo preview"
    photo_preview.allow_tags = True

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if form.changed_data:
            keys = [
                _ for _ in redis_instance.scan_iter(f"product:{form.instance.pk}:*")
            ]

            if keys:
                redis_instance.delete(*keys)
