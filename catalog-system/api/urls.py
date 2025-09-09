from django.urls import path
from .views import *

urlpatterns = [
    path("products/", get_products, name="get_products"),
    path("products/create/", create_product, name="create_product"),
    path("products/<str:id>", get_single_product, name="get_single_product"),
    path("products/update/<str:id>", update_product, name="update_product"),
    path("products/delete/<str:id>", delete_product, name="delete_product")
]