from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from unittest.mock import patch, MagicMock

from api.views import get_products, create_product, get_single_product, update_product, delete_product

# Create your tests here.
class GetProductsTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        
    def test_returns_200_with_serialized_data(self):
        req = self.factory.get("/products/")
        
        with patch("api.views.Product.objects.all") as all_mock, \
            patch("api.views.ProductSerializer") as serializer_cls:
            qs = object()
            all_mock.return_value = qs
            
            serializer_instance = MagicMock()
            serializer_instance.data = [
                 {"id": 1, "name": "A"},
                 {"id": 2, "name": "B"},
            ]
            serializer_cls.return_value = serializer_instance
            
            resp = get_products(req)
        
        # Called correctly
        all_mock.assert_called_once()
        serializer_cls.assert_called_once_with(qs, many=True)
        

        # Response assertions
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer_instance.data)
    
    def test_returns_500_on_exception(self):
        req = self.factory.get("/products/")

        with patch("api.views.Product.objects.all", side_effect=Exception("db down")) as all_mock, \
            patch("api.views.ProductSerializer") as serializer_cls:

            resp = get_products(req)
        
        all_mock.assert_called_once_with()
        serializer_cls.assert_not_called()
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
