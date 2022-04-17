from django.db import models

from product_categories.models import ProductCategoryModel


class ProductModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False, blank=False)
    photo = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        ProductCategoryModel, models.CASCADE, blank=False, null=False
    )

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        managed = False
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
