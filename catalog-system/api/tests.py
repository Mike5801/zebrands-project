from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

from api.views import get_products, create_product, get_single_product, update_product, delete_product

# Create your tests here.
class GetProductsTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        
    def test_gets_all_products_and_returns_200(self):
        # Define mock data and functions
        request = self.factory.get("/products/")
        with patch("api.views.Product.objects.all") as all_mock, \
            patch("api.views.ProductSerializer") as serializer_cls:
            query_set = object()
            all_mock.return_value = query_set
            
            serializer_instance = MagicMock()
            serializer_instance.data = [
                 {"id": 1, "name": "A"},
                 {"id": 2, "name": "B"},
            ]
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = get_products(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_mock.assert_called_once()
        serializer_cls.assert_called_once_with(query_set, many=True)
        self.assertEqual(response.data, serializer_instance.data)
    
    def test_db_fails_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.get("/products/")
        with patch("api.views.Product.objects.all", side_effect=Exception("db down")) as all_mock, \
            patch("api.views.ProductSerializer") as serializer_cls:

            # Test function with mock data
            response = get_products(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        all_mock.assert_called_once_with()
        serializer_cls.assert_not_called()

class GetSingleProductTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_gets_one_products_and_returns_200(self):
        # Define mock data and functions
        request = self.factory.get("/products/")
        with patch("api.views.Product.objects.all") as all_mock, \
            patch("api.views.ProductSerializer") as serializer_cls:
            query_set = object()
            all_mock.return_value = query_set
            
            serializer_instance = MagicMock()
            serializer_instance.data = [
                 {"id": 1, "name": "A"},
                 {"id": 2, "name": "B"},
            ]
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = get_products(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_mock.assert_called_once()
        serializer_cls.assert_called_once_with(query_set, many=True)
        self.assertEqual(response.data, serializer_instance.data)
    
    def test_returns_500_on_exception(self):
        # Define mock data and functions
        request = self.factory.get("/products/")
        with patch("api.views.Product.objects.all", side_effect=Exception("db down")) as all_mock, \
            patch("api.views.ProductSerializer") as serializer_cls:

            # Test function with mock data
            response = get_products(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        all_mock.assert_called_once_with()
        serializer_cls.assert_not_called()

class CreateProductTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
    
    def _admin_user(self):
        return SimpleNamespace(is_authenticated=True, is_staff=True)

    def _non_admin_user(self):
        return SimpleNamespace(is_authenticated=True, is_staff=False)

    def test_creates_product_and_returns_201(self):
        # Define mock data and functions
        mock_data = {
            "name": "created_product",
            "price": 200.00,
            "brand": "zebrands",
        }
        request = self.factory.post("/products/create", mock_data, format="json")
        force_authenticate(request, user=self._admin_user())
        with patch("api.views.ProductSerializer") as serializer_cls:
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.data = {
                "name": "created_product",
                "price": 200.00,
                "brand": "zebrands",
            }
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = create_product(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer_cls.assert_called_once_with(data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_called_once_with()
        self.assertEqual(response.data, serializer_instance.data)

    def test_non_admin_returns_401(self):
        # Define mock data and functions
        mock_data = {
            "name": "created_product",
            "price": 200.00,
            "brand": "zebrands",
        }
        request = self.factory.post("/products/create", mock_data, format="json")
        force_authenticate(request, user=self._non_admin_user())
        with patch("api.views.ProductSerializer") as serializer_cls:
            # Test function with mock data
            response = create_product(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        serializer_cls.assert_not_called()

    def test_admin_invalid_payload_returns_400(self):
        # Define mock data and functions
        mock_data = {
            "name": "created_product",
            "brand": "zebrands",
        }
        request = self.factory.post("/products/create", mock_data, format="json")
        force_authenticate(request, user=self._admin_user())
        with patch("api.views.ProductSerializer") as serializer_cls:
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = False
            serializer_instance.errors = { "price": ["This field may not be blank"] }
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = create_product(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        serializer_cls.assert_called_once_with(data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_not_called()

    def test_returns_500_on_exception(self):
        # Define mock data and functions
        mock_data = {
            "name": "created_product",
            "brand": "zebrands",
        }
        request = self.factory.post("/products/create", mock_data, format="json")
        force_authenticate(request, user=self._admin_user())
        # Test function with mock data
        with patch("api.views.ProductSerializer") as serializer_cls:
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.data = {
                "name": "created_product",
                "price": 200.00,
                "brand": "zebrands",
            }
            serializer_instance.save.side_effect = Exception("db down")
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = create_product(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer_cls.assert_called_once_with(data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()