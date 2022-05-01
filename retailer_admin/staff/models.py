from django.db import models

from shops.models import ShopModel
from users.models import UserModel


class StaffModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.id} сотрудник {self.shop.id}"

    class Meta:
        managed = False
        db_table = "staff"
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
