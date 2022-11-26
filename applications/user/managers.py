from django.db import models
from django.contrib.auth.models import BaseUserManager

class ManagerUsuario(BaseUserManager, models.Manager):
    def _create_user(self, username, nombres,password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            nombres = nombres,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, nombres, password=None, **extra_fields):
        return self._create_user(username, nombres, password, False, False, **extra_fields)

    def create_superuser(self, username,nombres, password=None, **extra_fields):
        return self._create_user(username,nombres ,password, True, True, **extra_fields)
