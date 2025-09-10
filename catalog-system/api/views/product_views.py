from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from api.models import Product
from api.serializers import ProductSerializer
from api.utils import notify_via_email

ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "error": {"type": "string", "example": "Error Code Message"},
    }
}

@extend_schema(
    tags=["Products"],
    summary="Get all products",
    description="Gets all the available products from the catalog",
    auth=[],
    responses={
        200: ProductSerializer(many=True),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_products(request):
    """
    Gets products from data base
    """
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            { "message": e },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@extend_schema(
    tags=["Products"],
    summary="Create a product",
    description="Creates a product in the catalog. You need to be authenticated and be an Admin to use this endpoint",
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
        400: OpenApiResponse(response=ERROR_SCHEMA),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product(request):
    """
    Create product in data base
    """
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            notify_via_email(serializer.instance.sku, serializer.instance.name, getattr(request.user, "email", None), "CREATE")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            { "message": e },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@extend_schema(
    tags=["Products"],
    description="Gets one product from the catalog based on the id",
    summary="Get a single product",
    auth=[],
    responses={
        200: ProductSerializer,        
        404: OpenApiResponse(response=ERROR_SCHEMA),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_single_product(request, id):
    """
    Get one product based on id from database
    """
    try:
        product = Product.objects.get(sku=id)
        product.views = product.views + 1
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(
            { "message": e },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@extend_schema(
    tags=["Products"],
    summary="Update a product",
    description="Updates a product in the catalog based on the id. You need to be authenticated and an Admin to use this endpoint",
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
        404: OpenApiResponse(response=ERROR_SCHEMA),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_product(request, id):
    """
    Update one product based on id from database
    """
    try:
        product = Product.objects.get(sku=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            notify_via_email(serializer.instance.sku, serializer.instance.name, getattr(request.user, "email", None), "UPDATE")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(
            { "message": e },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@extend_schema(
    tags=["Products"],
    summary="Delete a product",
    description="Deletes a product in the catalog based on the id. You need to be authenticated and an Admin to use this endpoint",
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
        404: OpenApiResponse(response=ERROR_SCHEMA),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_product(request, id):
    """
    Delete one product based on id from database
    """
    try:
        product = Product.objects.get(sku=id)
        product_sku = product.sku
        product_name = product.name
        product.delete()
        notify_via_email(product_sku, product_name, getattr(request.user, "email", None), "DELETE")
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(
            { "message": e },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
