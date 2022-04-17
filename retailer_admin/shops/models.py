from django.db import models


class ShopsModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.TextField(null=False, blank=False)
    street = models.TextField(null=False, blank=False)
    house = models.TextField(null=False, blank=False)
    floor = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Address: {self.city}, {self.street}, {self.house})"

    class Meta:
        managed = False
        db_table = "shops"
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
