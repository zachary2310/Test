from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.db.models.deletion import PROTECT


class Book(models.Model):
    writer = models.ForeignKey(
        "backend_auth.BackendUser",
        on_delete=PROTECT,
        related_name="owned_books",
    )
    name = models.CharField(max_length=100)
    synopsis = models.TextField()
    genre = models.ForeignKey(
        "core.BookGenre",
        on_delete=models.CASCADE,
    )
    release_date = models.DateTimeField()
    price = models.FloatField(
        validators=[
            MinValueValidator(0.0),
        ],
        null=False,
    )

    def __str__(self) -> str:
        return f"{self.name}/{self.writer}"

    def __repr__(self) -> str:
        return f"{self.id}/{self.name}/{self.writer}"

    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(price__gte=0.0),
                name="price_range",
            ),
        )


class BookGenre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "genres"
