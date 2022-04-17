from django.db import models


class UserModel(models.Model):
    REGULAR = "regular"
    STAFF = "staff"
    SUPERUSER = "superuser"

    ROLES = [
        (REGULAR, "Без привилегий"),
        (STAFF, "Штатный сотрудник"),
        (SUPERUSER, "Администратор"),
    ]

    id = models.BigAutoField(primary_key=True)
    email = models.TextField(null=False, unique=True)
    name = models.TextField(null=True)
    is_active = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    birthday = models.DateField(null=True)
    role = models.TextField(
        choices=ROLES,
        default=REGULAR,
    )

    def __str__(self):
        return f"{self.email} ({self.name} / {self.role})"

    class Meta:
        managed = False
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
