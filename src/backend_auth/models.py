from django.contrib.auth.models import AbstractUser
from django.db import models


class BackendUser(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(
        unique=True,
    )

    def __str__(self) -> str:
        return f"{self.username}"

    def __repr__(self) -> str:
        return f"{self.username}"
