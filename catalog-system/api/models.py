from django.db import models
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
        default=0
    )