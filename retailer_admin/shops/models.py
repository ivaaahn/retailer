from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import UserModel


class ShopModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.TextField(null=False, blank=False)
    street = models.TextField(null=False, blank=False)
    house = models.TextField(null=False, blank=False)
    floor = models.IntegerField(null=True, blank=True)
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
        return f"Address: {self.city}, {self.street}, {self.house})"

    class Meta:
        managed = False
        db_table = "shops"
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
