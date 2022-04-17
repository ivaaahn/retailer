from django.db import models


class ProductCategoryModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False, blank=False)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        managed = False
        db_table = "product_categories"
        verbose_name = "Категория продуктов"
        verbose_name_plural = "Категории продуктов"
