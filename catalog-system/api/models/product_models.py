from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

# Create your models here.
class Product(models.Model):
    """
    Model of the Product
    """
    sku = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    price = models.DecimalField(
        validators=[MinValueValidator(Decimal("0.01"))],
        decimal_places=2,
        max_digits=10,
        blank=False,
        null=False,
    )
    brand = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    views = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )