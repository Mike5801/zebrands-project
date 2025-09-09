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

class GetUsersTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        
    def test_admin_get_users_and_returns_200(self):
        # Define mock data and functions
        request = self.factory.get("/users/")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.all") as all_mock, \
            patch("api.views.user_views.UserSerializer") as serializer_cls:
            query_set = object()
            all_mock.return_value = query_set
            serializer_instance = MagicMock()
            serializer_instance.data = [
                {
                    "id": 1,
                    "username": "user",
                    "email": "user@test.com",
                    "is_active": True,
                    "is_staff": True,
                    "is_superuser": False,
                    "date_joined": "2025-09-09T05:37:41.464443Z",
                    "last_login": "2025-09-09T05:37:41.464443Z"
                },
                {
                    "id": 2,
                    "username": "user2",
                    "email": "user2@test.com",
                    "is_active": True,
                    "is_staff": True,
                    "is_superuser": False,
                    "date_joined": "2025-09-09T05:37:41.464443Z",
                    "last_login": "2025-09-09T05:37:41.464443Z"
                },
            ]
            serializer_cls.return_value = serializer_instance

            # Test function with mock data
            response = get_users(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_mock.assert_called_once()
        serializer_cls.assert_called_once_with(query_set, many=True)
        self.assertEqual(response.data, serializer_instance.data)

    def test_non_admin_get_all_users_db_fails_and_returns_403(self):
        # Define mock data and functions
        request = self.factory.get("/users/")
        force_authenticate(request, user=non_admin_user())
        with patch("api.views.user_views.User.objects.all", side_effect=Exception("db down")) as all_mock, \
            patch("api.views.user_views.UserSerializer") as serializer_cls:

            # Test function with mock data
            response = get_users(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        all_mock.assert_not_called()
        serializer_cls.assert_not_called()
        
    def test_admin_get_all_users_db_fails_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.get("/users/")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.all", side_effect=Exception("db down")) as all_mock, \
            patch("api.views.user_views.UserSerializer") as serializer_cls:

            # Test function with mock data
            response = get_users(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        all_mock.assert_called_once_with()
        serializer_cls.assert_not_called()
        
class GetSingleUser(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_admin_get_single_user_from_id_and_returns_200(self):
        # Define mock data and functions
        request = self.factory.get("/users/1")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock, \
            patch("api.views.user_views.UserSerializer") as serializer_cls:
            user = object()
            get_mock.return_value = user
            serializer_instance = MagicMock()
            serializer_instance.data = {
                "id": 1,
                "username": "user",
                "email": "user@test.com",
                "is_active": True,
                "is_staff": True,
                "is_superuser": False,
                "date_joined": "2025-09-09T05:37:41.464443Z",
                "last_login": "2025-09-09T05:37:41.464443Z"
            }
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = get_single_user(request, "1")
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_mock.assert_called_once_with(id="1")
        serializer_cls.assert_called_once_with(user)
        self.assertEqual(response.data, serializer_instance.data)

    def test_non_admin_get_single_user_db_fails_on_lookup_and_returns_403(self):
        # Define mock data and functions
        request = self.factory.get("/users/1")
        force_authenticate(request, user=non_admin_user())
        with patch("api.views.user_views.User.objects.get", side_effect=Exception("db down")) as get_mock, \
            patch("api.views.user_views.UserSerializer") as serializer_cls:

            # Test function with mock data
            response = get_single_user(request, "1")
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        get_mock.assert_not_called()
        serializer_cls.assert_not_called()
    
    def test_admin_get_single_user_not_found_and_returns_404(self):
        # Define mock data and functions
        request = self.factory.get("/users/nonexistant123")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get", side_effect=User.DoesNotExist) as get_mock, \
            patch("api.views.user_views.UserSerializer") as serializer_cls:
            
            # Test function with mock data
            response = get_single_user(request, "nonexistant123")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        get_mock.assert_called_once_with(id="nonexistant123")
        serializer_cls.assert_not_called()
    
    def test_admin_get_single_user_db_fails_on_lookup_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.get("/users/1")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get", side_effect=Exception("db down")) as get_mock, \
            patch("api.views.user_views.UserSerializer") as serializer_cls:

            # Test function with mock data
            response = get_single_user(request, "1")
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(id="1")
        serializer_cls.assert_not_called()

class CreateUserTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_creates_user_and_returns_201(self):
        # Define mock data and functions
        mock_data = {
            "username": "new_user",
            "email": "new_user@email.com",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "password": "user_password",
            "is_staff": True
        }
        request = self.factory.post("/users/create", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.UserInputSerializer") as serializer_cls, \
            patch("api.views.user_views.User.objects.filter") as get_mock:
            user = None
            get_mock.return_value = user
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.data = {
                "username": "new_user",
                "email": "new_user@email.com",
                "first_name": "user_first_name",
                "last_name": "user_last_name",
                "password": "user_password",
                "is_staff": True
            }
            serializer_cls.return_value = serializer_instance
            serializer_instance.save = MagicMock()
            
            # Test function with mock data
            response = create_user(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        get_mock.assert_called_once_with(username=mock_data["username"])
        serializer_cls.assert_called_once_with(data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_called_once_with()
        self.assertEqual(response.data, serializer_instance.data)

    def test_creates_user_same_username_fails_and_returns_201(self):
        # Define mock data and functions
        mock_data = {
            "username": "user",
            "email": "new_user@email.com",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "password": "user_password",
            "is_staff": True
        }
        request = self.factory.post("/users/create", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.UserInputSerializer") as serializer_cls, \
            patch("api.views.user_views.User.objects.filter") as get_mock:
            user = SimpleNamespace()
            get_mock.return_value = user
            serializer_instance = MagicMock()
            serializer_cls.return_value = serializer_instance
            serializer_instance.save = MagicMock()
            
            # Test function with mock data
            response = create_user(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        get_mock.assert_called_once_with(username=mock_data["username"])
        serializer_cls.assert_not_called()
        serializer_instance.is_valid.assert_not_called()
        serializer_instance.save.asser_not_called()

    def test_non_admin_creates_user_and_returns_403(self):
        # Define mock data and functions
        mock_data = {
            "username": "new_user",
            "email": "new_user@email.com",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "password": "user_password",
            "is_staff": True
        }
        request = self.factory.post("/users/create", mock_data, format="json")
        force_authenticate(request, user=non_admin_user())
        with patch("api.views.user_views.UserInputSerializer") as serializer_cls:
            serializer_cls.save = MagicMock()
            # Test function with mock data
            response = create_user(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        serializer_cls.assert_not_called()
        serializer_cls.save.assert_not_called()

    def test_admin_create_user_invalid_payload_and_returns_400(self):
        # Define mock data and functions
        mock_data = {
            "username": "new_user",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "password": "user_password",
            "is_staff": True
        }
        request = self.factory.post("/users/create", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.UserInputSerializer") as serializer_cls, \
            patch("api.views.user_views.User.objects.filter") as get_mock:
            user = None
            get_mock.return_value = user
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = False
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = create_user(request)
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        get_mock.assert_called_once_with(username=mock_data["username"])
        serializer_cls.assert_called_once_with(data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_not_called()

    def test_create_user_db_fails_and_returns_500(self):
        # Define mock data and functions
        mock_data = {
            "username": "new_user",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "password": "user_password",
            "is_staff": True
        }
        request = self.factory.post("/users/create", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        # Test function with mock data
        with patch("api.views.user_views.UserInputSerializer") as serializer_cls, \
            patch("api.views.user_views.User.objects.filter") as get_mock:
            user = None
            get_mock.return_value = user
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.save = MagicMock(side_effect=Exception("db down"))
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = create_user(request)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(username=mock_data["username"])
        serializer_cls.assert_called_once_with(data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()

class UpdateUserTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_admin_update_user_and_returns_200(self):
        # Define mock data and functions
        mock_data = {
            "username": "updated_user",
            "first_name": "updated_first_name",
            "email": "updated_user@email.com",
            "last_name": "updated_last_name",
            "password": "updated_password",
            "is_staff": True
        }
        request = self.factory.put("/users/update/1", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock, \
            patch("api.views.user_views.UserInputSerializer") as serializer_cls:
            user = SimpleNamespace(
                username="found_user",
                first_name="found_first_name",
                last_name="found_last_name",
                is_staff=True
            )
            user.is_superuser = False
            get_mock.return_value = user 
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.data = {
                "username": "updated_user",
                "first_name": "updated_first_name",
                "last_name": "updated_last_name",
                "password": "updated_password",
                "is_staff": True
            }
            serializer_instance.save = MagicMock()
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = update_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_mock.assert_called_once_with(id="1")
        serializer_cls.assert_called_once_with(user, data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_called_once_with()
        self.assertEqual(response.data, serializer_instance.data)
        
    def test_admin_update_superuser_fails_and_returns_400(self):
        # Define mock data and functions
        mock_data = {
            "username": "updated_user",
            "first_name": "updated_first_name",
            "email": "updated_user@email.com",
            "last_name": "updated_last_name",
            "password": "updated_password",
            "is_staff": True
        }
        request = self.factory.put("/users/update/1", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock, \
            patch("api.views.user_views.UserInputSerializer") as serializer_cls:
            user = SimpleNamespace(
                username="found_user",
                first_name="found_first_name",
                last_name="found_last_name",
                is_staff=True
            )
            user.is_superuser = True
            get_mock.return_value = user 
            serializer_instance = MagicMock()
            serializer_instance.save = MagicMock()
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = update_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        get_mock.assert_called_once_with(id="1")
        serializer_cls.assert_not_called()
        serializer_instance.is_valid.assert_not_called()
        serializer_instance.save.assert_not_called()

    def test_non_admin_update_user_and_returns_200(self):
        # Define mock data and functions
        mock_data = {
            "username": "updated_user",
            "first_name": "updated_first_name",
            "email": "updated_user@email.com",
            "last_name": "updated_last_name",
            "password": "updated_password",
            "is_staff": True
        }
        request = self.factory.put("/users/update/1", mock_data, format="json")
        force_authenticate(request, user=non_admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock, \
            patch("api.views.user_views.UserInputSerializer") as serializer_cls:
            
            # Test function with mock data
            response = update_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        get_mock.assert_not_called()
        serializer_cls.assert_not_called()

    def test_update_user_does_not_exist_and_returns_404(self):
        # Define mock data and functions
        mock_data = {
            "username": "updated_user",
            "first_name": "updated_first_name",
            "email": "updated_user@email.com",
            "last_name": "updated_last_name",
            "password": "updated_password",
            "is_staff": True
        }
        request = self.factory.put("/users/update/doesnotexist", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get", side_effect=User.DoesNotExist) as get_mock, \
            patch("api.views.user_views.UserInputSerializer") as serializer_cls:

            # Test function with mock data
            response = update_user(request, "doesnotexist")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        get_mock.assert_called_once_with(id="doesnotexist")
        serializer_cls.assert_not_called()
    
    def test_update_user_payload_invalid_and_returns_400(self):
        # Define mock data and functions
        mock_data = {
            "username": "updated_user",
            "first_name": 1,
            "last_name": "updated_last_name",
            "email": "updated_user@email.com",
            "password": "updated_password",
            "is_staff": True
        }
        request = self.factory.put("/users/update/1", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock, \
            patch("api.views.user_views.UserInputSerializer") as serializer_cls:
            user = SimpleNamespace(
                username="found_user",
                first_name=1,
                last_name="found_last_name",
                email="updated_user@email.com",
                is_staff=True
            )
            user.is_superuser = False
            get_mock.return_value = user
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = False
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = update_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        get_mock.assert_called_once_with(id="1")
        serializer_cls.assert_called_once_with(user, data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_not_called()

    
    def test_update_user_db_fails_on_lookup_and_returns_500(self):
        # Define mock data and functions
        mock_data = {
            "username": "updated_user",
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "email": "updated_user@email.com",
            "password": "updated_password",
            "is_staff": True
        }
        request = self.factory.put("/users/update/1", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get", side_effect=Exception("db down")) as get_mock, \
            patch("api.views.user_views.UserInputSerializer") as serializer_cls:

            # Test function with mock data
            response = update_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(id="1")
        serializer_cls.assert_not_called()
        
    def test_update_user_db_fails_on_save_and_returns_500(self):
        # Define mock data and functions
        mock_data = {
            "username": "updated_user",
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "email": "updated_user@email.com",
            "password": "updated_password",
            "is_staff": True
        }
        request = self.factory.put("/users/update/1", mock_data, format="json")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock, \
            patch("api.views.user_views.UserInputSerializer") as serializer_cls:
            user = SimpleNamespace(
                username="found_user",
                first_name=1,
                last_name="found_last_name",
                email="updated_user@email.com",
                is_staff=True
            )
            user.is_superuser = False
            get_mock.return_value = user
            serializer_instance = MagicMock()
            serializer_instance.is_valid.return_value = True
            serializer_instance.save = MagicMock(side_effect=Exception("db down"))
            serializer_cls.return_value = serializer_instance
            
            # Test function with mock data
            response = update_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(id="1")
        serializer_cls.assert_called_once_with(user, data=mock_data)
        serializer_instance.is_valid.assert_called_once_with()
        serializer_instance.save.assert_called_once()

class DeleteUserTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
    
    def test_admin_delete_user_and_returns_204(self):
        # Define mock data and functions
        request = self.factory.delete("/users/delete/1")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock:
            user = SimpleNamespace(
                username="found_user",
                first_name=1,
                last_name="found_last_name",
                email="updated_user@email.com",
                is_staff=True
            )
            user.is_superuser = False
            user.delete = MagicMock()
            get_mock.return_value = user

            # Test function with mock data
            response = delete_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        get_mock.assert_called_once_with(id="1")
        user.delete.assert_called_once()
    
    def test_admin_delete_super_user_fails_and_returns_400(self):
        # Define mock data and functions
        request = self.factory.delete("/users/delete/1")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock:
            user = SimpleNamespace(
                username="found_user",
                first_name=1,
                last_name="found_last_name",
                email="updated_user@email.com",
                is_staff=True
            )
            user.is_superuser = True
            user.delete = MagicMock()
            get_mock.return_value = user

            # Test function with mock data
            response = delete_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        get_mock.assert_called_once_with(id="1")
        user.delete.assert_not_called()

    def test_non_admin_delete_user_and_returns_403(self):
        # Define mock data and functions
        request = self.factory.delete("/users/delete/1")
        force_authenticate(request, user=non_admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock:
            user = SimpleNamespace(
                username="found_user",
                first_name=1,
                last_name="found_last_name",
                email="updated_user@email.com",
                is_staff=True
            )
            user.is_superuser = False
            user.delete = MagicMock()
            get_mock.return_value = user

            # Test function with mock data
            response = delete_user(request, "123")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        get_mock.assert_not_called()
        user.delete.assert_not_called()

    def test_delete_user_not_found_and_returns_404(self):
        # Define mock data and functions
        request = self.factory.delete("/users/delete/doesnotexist")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get", side_effect=User.DoesNotExist) as get_mock:
            user = SimpleNamespace(
                username="found_user",
                first_name=1,
                last_name="found_last_name",
                email="updated_user@email.com",
                is_staff=True
            )
            user.is_superuser = False
            user.delete = MagicMock()
            get_mock.return_value = user

            # Test function with mock data
            response = delete_user(request, "doesnotexist")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        get_mock.assert_called_once_with(id="doesnotexist")
        user.delete.assert_not_called()

    def test_delete_user_db_fails_on_lookup_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.delete("/users/delete/1")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get", side_effect=Exception("db down")) as get_mock:

            # Test function with mock data
            response = delete_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(id="1")
    
    def test_delete_user_db_fails_on_delete_and_returns_500(self):
        # Define mock data and functions
        request = self.factory.delete("/users/delete/1")
        force_authenticate(request, user=admin_user())
        with patch("api.views.user_views.User.objects.get") as get_mock:
            user = SimpleNamespace()
            user.is_superuser = False
            user.delete = MagicMock(side_effect=Exception("db down"))
            get_mock.return_value = user

            # Test function with mock data
            response = delete_user(request, "1")
            
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        get_mock.assert_called_once_with(id="1")
        user.delete.assert_called_once()