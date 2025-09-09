from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from .models import Product
from .serializer import ProductSerializer

ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "error": {"type": "string", "example": "Error Code Message"},
    }
}

@extend_schema(
    tags=["Products"],
    summary="Get all products",
    auth=[],
    responses={
        200: ProductSerializer(many=True),
    }
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_products(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=["Products"],
    summary="Create a product",
    request=inline_serializer(
        name="ProductInput",
        fields={
            "name": serializers.CharField(),
            "price": serializers.DecimalField(
                max_digits=10,
                decimal_places=2
            ),
            "brand": serializers.CharField()
        }
    ),
    examples=[
        OpenApiExample(
            "Create product example",
            value={
                "name": "test_product",
                "price": 100,
                "brand": "zebrands"
            },
            request_only=True
        )
    ],
    responses={
        201: ProductSerializer,        
        400: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["POST"])
def create_product(request):
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=["Products"],
    summary="Get a single product",
    auth=[],
    responses={
        200: ProductSerializer,        
        404: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_single_product(request, id):
    try:
        try:
            product = Product.objects.get(sku=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
    tags=["Products"],
    summary="Create a product",
    request=inline_serializer(
        name="ProductInput",
        fields={
            "name": serializers.CharField(),
            "price": serializers.DecimalField(
                max_digits=10,
                decimal_places=2
            ),
            "brand": serializers.CharField()
        }
    ),
    examples=[
        OpenApiExample(
            "Create product example",
            value={
                "name": "updated_product",
                "price": 100,
                "brand": "zebrands"
            },
            request_only=True
        )
    ],
    responses={
        200: ProductSerializer,        
        400: OpenApiResponse(response=ERROR_SCHEMA),
        404: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["PUT"])
def update_product(request, id):
    try:
        try:
            product = Product.objects.get(sku=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=["Products"],
    summary="Delete a product",
    responses={
        204: OpenApiResponse(response={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "No Content"
                }
            }
        }),        
        404: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["DELETE"])
def delete_product(request, id):
    try:
        try:
            product = Product.objects.get(sku=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
