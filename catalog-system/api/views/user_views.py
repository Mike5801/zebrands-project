from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from api.serializers import UserInputSerializer, UserSerializer

User = get_user_model()

ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "error": {"type": "string", "example": "Error Code Message"},
    }
}

@extend_schema(
    tags=["Users"],
    summary="Get all users",
    description="Get all the users in the system",
    responses={
        200: UserSerializer(many=True),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
    tags=["Users"],
    summary="Create an admin user",
    description="Creates an admin user in the database. You need to be authenticated and an Admin to use this endpoint",
    request=UserInputSerializer,
    examples=[
        OpenApiExample(
            "Create user example",
            value={
                "username": "new_user",
                "email": "new_user@email.com",
                "first_name": "user_first_name",
                "last_name": "user_last_name",
                "password": "user_password"
            },
            request_only=True
        )
    ],
    responses={
        201: UserSerializer,
        400: OpenApiResponse(response=ERROR_SCHEMA),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_user(request):
    try:
        user = User.objects.filter(username=request.data["username"])
        if user:
            return Response(
                { "message": f"User with username {request.data['username']} already exists" }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        request.data["is_staff"] = True
        serializer = UserInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
    tags=["Users"],
    description="Get one user from the system based on the id",
    summary="Get a single user",
    responses={
        200: UserSerializer,        
        404: OpenApiResponse(response=ERROR_SCHEMA),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_single_user(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=["Users"],
    summary="Update a user",
    description="Update a user in the system based on the id. You need to be authenticated and an Admin to use this endpoint",
    request=UserInputSerializer,
    examples=[
        OpenApiExample(
            "Create user example",
            value={
                "username": "updated_user",
                "email": "updated_user@email.com",
                "first_name": "updated_first_name",
                "last_name": "updated_last_name",
                "password": "updated_password",
                "is_staff": True
            },
            request_only=True
        )
    ],
    responses={
        200: UserSerializer,        
        400: OpenApiResponse(response=ERROR_SCHEMA),
        404: OpenApiResponse(response=ERROR_SCHEMA),
        500: OpenApiResponse(response=ERROR_SCHEMA)
    }
)
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
        if user.is_superuser == True:
            return Response(
                { "message": "Can't update supersusers, only admins." },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserInputSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=["Users"],
    summary="Delete a user",
    description="Delete a user in the system based on the id. You need to be authenticated and an Admin to use this endpoint",
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
def delete_user(request, id):
    try:
        user = User.objects.get(id=id)
        if user.is_superuser == True:
            return Response(
                { "message": "Can't delete supersusers, only admins." },
                status=status.HTTP_400_BAD_REQUEST
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)