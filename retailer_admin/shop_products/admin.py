import redis
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import SimpleListFilter

# Register your models here.
from shop_products.models import ShopProductModel
from shops.models import ShopModel

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class ShopProductsFilter(SimpleListFilter):
    title = "моим магазинам"  # a label for our filter
    parameter_name = "pages"  # you can put anything here

    def lookups(self, request, model_admin):
        res = []

        for shop in ShopModel.objects.filter(pk__in=request.user.shop_set.all()):
            res.append(
                (
                    shop.id,
                    str(shop),
                )
            )

        return res

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(shop=self.value())

        return queryset.distinct().filter(shop__in=request.user.shop_set.all())


def product_name(obj):
    return obj.product.name


def product_id(obj):
    return obj.product.pk


def product_category(obj):
    return obj.product.category


product_name.short_description = "Наименование"
product_category.short_description = "Категория"
product_id.short_description = "Идентификатор"


@admin.register(ShopProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        product_name,
        product_id,
        product_category,
        "price",
        "qty",
    )

    list_filter = (
        "product__category",
        ShopProductsFilter,
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(shop__in=request.user.shop_set.all())
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "shop":
            kwargs["queryset"] = ShopModel.objects.filter(
                pk__in=request.user.shop_set.all()
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields["shop"] = forms.ModelChoiceField(
    #         queryset=ShopModel.objects.filter(pk__in=request.user.shop_set.all())
    #     )
    #     return form

    @staticmethod
    def _make_shop_product_key(product_id: int, shop_id: int) -> str:
        return f"product:{product_id}:{shop_id}"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if form.changed_data:
            redis_instance.delete(
                self._make_shop_product_key(form.data["product"], form.data["shop"])
            )
