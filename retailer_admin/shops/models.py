from django.db import models
from django.utils.translation import gettext_lazy as _

from shop_addresses.models import ShopAddressModel
from users.models import UserModel


class ShopModel(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="Идентификатор магазина")
    address = models.ForeignKey(
        ShopAddressModel, models.CASCADE, verbose_name="Адрес", blank=False, null=False
    )
    staff = models.ManyToManyField(
        UserModel,
        verbose_name=_("Сотрудники магазина"),
        blank=True,
        help_text=_("Сотрудники данного магазина"),
        related_name="shop_set",
        related_query_name="shops",
        through="staff.StaffModel",
    )

    def __str__(self):
        return f"М-{self.id} ({self.address})"

    class Meta:
        managed = False
        db_table = "shops"
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
