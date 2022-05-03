from django.db import models


class ShopAddressModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.TextField(verbose_name="Город", null=False, blank=False)
    street = models.TextField(verbose_name="Улица", null=False, blank=False)
    house = models.TextField(verbose_name="Дом", null=False, blank=False)
    floor = models.IntegerField(verbose_name="Этаж", null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}"

    class Meta:
        managed = False
        db_table = "shop_addresses"
        verbose_name = "Адрес магазина"
        verbose_name_plural = "Адреса магазинов"
