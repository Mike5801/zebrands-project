from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

from api.views import *

def admin_user():
    return SimpleNamespace(is_authenticated=True, is_staff=True)

def non_admin_user():
    return SimpleNamespace(is_authenticated=True, is_staff=False)
# Create your tests here.
class GetProductsTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        
    def test_get_all_products_and_returns_200(self):
        # Define mock data and functions
        request = self.factory.get("/products/")
        with patch("api.views.product_views.Product.objects.all") as all_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:
            query_set = object()
            all_mock.return_value = query_set
            
            serializer_instance = MagicMock()
            serializer_instance.data = [
                {
                    "sku": "123",
                    "name": "test_product_1",
                    "price": 100,
                    "brand": "zebrands",
                    "views": 10
                },
                {
                    "sku": "234",
                    "name": "test_product_2",
                    "price": 100,
                    "brand": "zebrands",
                    "views": 200
                },
            ]
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = get_products(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_mock.assert_called_once()
        serializer_cls.assert_called_once_with(query_set, many=True)
        self.assertEqual(response.data, serializer_instance.data)
    
    def test_get_all_products_db_fails_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.get("/products/")
        with patch("api.views.product_views.Product.objects.all", side_effect=Exception("db down")) as all_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:

            # Test function with mock data
            response = get_products(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        all_mock.assert_called_once_with()
        serializer_cls.assert_not_called()

class GetSingleProductTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_single_product_from_id_and_returns_200(self):
        # Define mock data and functions
        request = self.factory.get("/products/123")
        with patch("api.views.product_views.Product.objects.get") as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:
            product = SimpleNamespace(views=10)
            product.save = MagicMock()
            get_mock.return_value = product
            serializer_instance = MagicMock()
            serializer_instance.data = {
                "sku": "123",
                "name": "test_product_1",
                "price": 100,
                "brand": "zebrands",
                "views": 11
            }
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = get_single_product(request, "123")
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert product.views == 11
        product.save.assert_called_once()
        get_mock.assert_called_once_with(sku="123")
        serializer_cls.assert_called_once_with(product)
        self.assertEqual(response.data, serializer_instance.data)
    
    def test_get_single_product_not_found_and_returns_404(self):
        # Define mock data and functions
        request = self.factory.get("/products/nonexistant123")
        with patch("api.views.product_views.Product.objects.get", side_effect=Product.DoesNotExist) as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:
            
            # Test function with mock data
            response = get_single_product(request, "nonexistant123")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        get_mock.assert_called_once_with(sku="nonexistant123")
        serializer_cls.assert_not_called()
    
    def test_get_single_product_db_fails_on_lookup_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.get("/products/123")
        with patch("api.views.product_views.Product.objects.get", side_effect=Exception("db down")) as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:

            # Test function with mock data
            response = get_single_product(request, "123")
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(sku="123")
        serializer_cls.assert_not_called()
    
class CreateProductTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_creates_product_and_returns_201(self):
        # Define mock data and functions
        mock_data = {
            "name": "created_product",
            "price": 200.00,
            "brand": "zebrands",
        }
        request = self.factory.post("/products/create", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.ProductSerializer") as serializer_cls:
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

    def test_non_admin_creates_product_and_returns_403(self):
        # Define mock data and functions
        mock_data = {
            "name": "created_product",
            "price": 200.00,
            "brand": "zebrands",
        }
        request = self.factory.post("/products/create", mock_data, format="json")
        force_authenticate(request, user=non_admin_user())
        with patch("api.views.product_views.ProductSerializer") as serializer_cls:
            # Test function with mock data
            response = create_product(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        serializer_cls.assert_not_called()

    def test_admin_create_product_invalid_payload_and_returns_400(self):
        # Define mock data and functions
        mock_data = {
            "name": "created_product",
            "brand": "zebrands",
        }
        request = self.factory.post("/products/create", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.ProductSerializer") as serializer_cls:
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = False
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = create_product(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        serializer_cls.assert_called_once_with(data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_not_called()

    def test_create_product_db_failes_and_returns_500(self):
        # Define mock data and functions
        mock_data = {
            "name": "created_product",
            "brand": "zebrands",
        }
        request = self.factory.post("/products/create", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        # Test function with mock data
        with patch("api.views.product_views.ProductSerializer") as serializer_cls:
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.data = {
                "name": "created_product",
                "price": 200.00,
                "brand": "zebrands",
            }
            serializer_instance.save = MagicMock(side_effect=Exception("db down"))
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = create_product(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer_cls.assert_called_once_with(data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        
class UpdateProductTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_admin_update_product_and_returns_200(self):
        # Define mock data and functions
        mock_data = {
            "name": "updated_product",
            "price": 200.00,
            "brand": "zebrands",
        }
        request = self.factory.put("/products/update/123", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get") as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:
            product = SimpleNamespace(
                name="product",
                price=100,
                brand="zebrands"
            )
            get_mock.return_value = product
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.data = {
                "name": "updated_product",
                "price": 200.00,
                "brand": "zebrands",
            }
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = update_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_mock.assert_called_once_with(sku="123")
        serializer_cls.assert_called_once_with(product, data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_called_once_with()
        self.assertEqual(response.data, serializer_instance.data)
        
    def test_non_admin_update_product_and_returns_200(self):
        # Define mock data and functions
        mock_data = {
            "name": "updated_product",
            "price": 200.00,
            "brand": "zebrands",
        }
        request = self.factory.put("/products/update/123", mock_data, format="json")
        force_authenticate(request, user=non_admin_user())
        with patch("api.views.product_views.Product.objects.get") as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:
            
            # Test function with mock data
            response = update_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        get_mock.assert_not_called()
        serializer_cls.assert_not_called()

    def test_update_product_does_not_exist_and_returns_404(self):
        # Define mock data and functions
        mock_data = {
            "name": "updated_product",
            "price": 200.00,
            "brand": "zebrands",
        }
        request = self.factory.put("/products/update/doesnotexist", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get", side_effect=Product.DoesNotExist) as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:

            # Test function with mock data
            response = update_product(request, "doesnotexist")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        get_mock.assert_called_once_with(sku="doesnotexist")
        serializer_cls.assert_not_called()
    
    def test_update_product_payload_invalid_and_returns_400(self):
        # Define mock data and functions
        mock_data = {
            "name": "updated_product",
            "brand": "zebrands",
        }
        request = self.factory.put("/products/update/123", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get") as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:
            product = SimpleNamespace(
                name="product",
                price=100,
                brand="zebrands"
            )
            get_mock.return_value = product
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = False
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = update_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        get_mock.assert_called_once_with(sku="123")
        serializer_cls.assert_called_once_with(product, data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_not_called()

    
    def test_update_product_db_fails_on_lookup_and_returns_500(self):
        # Define mock data and functions
        mock_data = {
            "name": "updated_product",
            "price": 200.00,
            "brand": "zebrands",
        }
        request = self.factory.put("/products/update/123", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get", side_effect=Exception("db down")) as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:

            # Test function with mock data
            response = update_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(sku="123")
        serializer_cls.assert_not_called()
        
    def test_update_product_db_fails_on_save_and_returns_500(self):
        # Define mock data and functions
        mock_data = {
            "name": "updated_product",
            "price": 100,
            "brand": "zebrands",
        }
        request = self.factory.put("/products/update/123", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get") as get_mock, \
            patch("api.views.product_views.ProductSerializer") as serializer_cls:
            product = SimpleNamespace(
                name="product",
                price=100,
                brand="zebrands"
            )
            get_mock.return_value = product
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.save = MagicMock(side_effect=Exception("db down"))
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = update_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(sku="123")
        serializer_cls.assert_called_once_with(product, data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_called_once()

class DeleteProductTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
    
    def test_admin_delete_product_and_returns_204(self):
        # Define mock data and functions
        request = self.factory.delete("/products/delete/123")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get") as get_mock:
            product = SimpleNamespace()
            product.delete = MagicMock()
            get_mock.return_value = product
            # Test function with mock data
            response = delete_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        get_mock.assert_called_once_with(sku="123")
        product.delete.assert_called_once()
    
    def test_non_admin_delete_product_and_returns_403(self):
        # Define mock data and functions
        request = self.factory.delete("/products/delete/123")
        force_authenticate(request, user=non_admin_user())
        with patch("api.views.product_views.Product.objects.get") as get_mock:
            product = SimpleNamespace()
            product.delete = MagicMock()
            get_mock.return_value = product

            # Test function with mock data
            response = delete_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        get_mock.assert_not_called()
        product.delete.asser()

    def test_delete_product_not_found_and_returns_404(self):
        # Define mock data and functions
        request = self.factory.delete("/products/delete/doesnotexist")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get", side_effect=Product.DoesNotExist) as get_mock:

            # Test function with mock data
            response = delete_product(request, "doesnotexist")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        get_mock.assert_called_once_with(sku="doesnotexist")


    def test_delete_product_db_fails_on_lookup_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.delete("/products/delete/123")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get", side_effect=Exception("db down")) as get_mock:

            # Test function with mock data
            response = delete_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(sku="123")
    
    def test_delete_product_db_fails_on_delete_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.delete("/products/delete/123")
        force_authenticate(request, user=admin_user())
        with patch("api.views.product_views.Product.objects.get") as get_mock:
            product = SimpleNamespace()
            product.delete = MagicMock(side_effect=Exception("db down"))
            get_mock.return_value = product

            # Test function with mock data
            response = delete_product(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(sku="123")
        product.delete.assert_called_once()