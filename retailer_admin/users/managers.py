from django.contrib.auth.models import BaseUserManager


class UserModelManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        return self.create_user(
            email, password, role="superuser", is_active=True, **extra_fields
        )
