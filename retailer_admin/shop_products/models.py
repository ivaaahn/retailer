from django.db import models

from products.models import ProductModel
from shops.models import ShopModel


class ShopProductModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(
        ShopModel, models.CASCADE, verbose_name="Магазин", blank=False, null=False
    )
    product = models.ForeignKey(
        ProductModel, models.CASCADE, verbose_name="Продукт", blank=False, null=False
    )
    price = models.IntegerField(verbose_name="Цена", null=False, blank=False)
    qty = models.FloatField(verbose_name="Количество", null=True, blank=False)

    def __str__(self):
        return f"{self.product.name} / {self.product.category} - {self.price} руб., [осталось {self.qty} шт.]"

    class Meta:
        managed = False
        db_table = "shop_products"
        verbose_name = "Продукт магазина"
        verbose_name_plural = "Продукты магазинов"
