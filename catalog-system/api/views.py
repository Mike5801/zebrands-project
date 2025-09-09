from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializer import ProductSerializer

@api_view(["GET"])
def get_products(request):
    return Response(ProductSerializer({""}).data)