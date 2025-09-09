from django.urls import path
from .views import *

urlpatterns = [
    # Products
    path("products/", get_products, name="get_products"),
    path("products/create/", create_product, name="create_product"),
    path("products/<str:id>", get_single_product, name="get_single_product"),
    path("products/update/<str:id>", update_product, name="update_product"),
    path("products/delete/<str:id>", delete_product, name="delete_product"),

    # Users
    path("users/", get_users, name="get_users"),
    path("users/create/", create_user, name="create_user"),
    path("users/<str:id>", get_single_user, name="get_single_user"),
    path("users/update/<str:id>", update_user, name="update_user"),
    path("users/delete/<str:id>", delete_user, name="delete_user"),
]