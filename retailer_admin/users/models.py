from django.contrib.auth.hashers import BCryptPasswordHasher
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models
from passlib.hash import bcrypt
from django.utils.translation import gettext_lazy as _

from .managers import UserModelManager


class CustomBCryptHasher(BCryptPasswordHasher):
    def encode(self, password: str, **_):
        return bcrypt.hash(password)

    def verify(self, password: str, encoded: str):
        return bcrypt.verify(password, encoded)


class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey("UserModel", on_delete=models.CASCADE)

    class Meta:
        db_table = "users_groups"


class PermissionUser(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    user = models.ForeignKey("UserModel", on_delete=models.CASCADE)

    class Meta:
        db_table = "users_user_permissions"


class UserModel(AbstractBaseUser, PermissionsMixin):
    CLIENT = "client"
    STAFF = "staff"
    SUPERUSER = "superuser"

    ROLE_CHOICES = (
        (CLIENT, "Клиент"),
        (STAFF, "Сотрудник"),
        (SUPERUSER, "Администратор"),
    )

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(null=False, unique=True)
    name = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    birthday = models.DateField(null=True)
    role = models.TextField(
        choices=ROLE_CHOICES,
        blank=False,
        null=False,
        default=STAFF,
    )

    objects = UserModelManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("Группы пользователей"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
        through=GroupUser,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
        through=PermissionUser,
    )

    def __str__(self):
        return f"{self.email} ({self.name} / {self.role})"

    @property
    def is_staff(self) -> bool:
        return self.role in (self.STAFF, self.SUPERUSER)

    @property
    def is_superuser(self) -> bool:
        return self.role == self.SUPERUSER

    class Meta:
        managed = False
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def set_password(self, raw_password: str):
        self.password = self.make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password: str):
        return CustomBCryptHasher().verify(raw_password, self.password)

    @staticmethod
    def make_password(password: str, **_):
        return CustomBCryptHasher().encode(password)
