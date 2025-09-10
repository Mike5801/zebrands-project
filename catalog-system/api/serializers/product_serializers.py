from rest_framework import serializers
from api.models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Product serialzer used as main schema for products
    """
    class Meta:
        model = Product
        fields = "__all__"