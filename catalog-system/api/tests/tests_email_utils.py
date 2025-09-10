from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from api.utils import notify_via_email
from types import SimpleNamespace

class EmailNotificationTests(SimpleTestCase):
    def setUp(self):
        return super().setUp()
    
    def test_send_email_successfully(self):
        # Define mock data and functions
        with patch("api.utils.email_utils.User.objects.all") as all_mock, \
            patch("api.utils.email_utils.send_mail") as send_email_mock, \
            patch("api.utils.email_utils.EMAIL_HOST_USER", "noreply@test.com"):
            product_id = "123"
            product_name = "test_product"
            owner = "user@test.com"
            action = "MY_ACTION"
            existing_users = [
                SimpleNamespace(
                    id=1,
                    username="user",
                    email="user@test.com",
                    is_active=True,
                    is_staff=True,
                    is_superuser=False,
                    date_joined="2025-09-09T05:37:41.464443Z",
                    last_login="2025-09-09T05:37:41.464443Z"
                ),
                SimpleNamespace(
                    id=2,
                    username="user2",
                    email="user2@test.com",
                    is_active=True,
                    is_staff=True,
                    is_superuser=False,
                    date_joined="2025-09-09T05:37:41.464443Z",
                    last_login="2025-09-09T05:37:41.464443Z"
                ),
            ]
            all_mock.return_value = existing_users
            formatted_subject = f"Product catalog has been recently changed by: {owner}"
            expected_receivers = [
                "user@test.com",
                "user2@test.com"
            ]
            
            # Test function with mock data
            notify_via_email(
                product_id,
                product_name,
                owner,
                action
            )
        
        # Assertions
        all_mock.assert_called_once()
        send_email_mock.assert_called_once()
        subject, message, from_email, receivers, fail_silently = send_email_mock.call_args[0]
        assert formatted_subject == subject
        assert "MY_ACTION" in message and "123" in message and "test_product" in message and "user@test.com" in message
        assert from_email == "noreply@test.com"
        assert receivers == expected_receivers
        assert fail_silently is True

    def test_send_email_db_fails(self):
        with patch("api.utils.email_utils.User.objects.all", side_effect=Exception("db down")) as all_mock, \
            patch("api.utils.email_utils.send_mail") as send_email_mock, \
            patch("api.utils.email_utils.EMAIL_HOST_USER", "noreply@test.com"):
            product_id = "123"
            product_name = "test_product"
            owner = "user@test.com"
            action = "MY_ACTION"
            existing_users = [
                SimpleNamespace(
                    id=1,
                    username="user",
                    email="user@test.com",
                    is_active=True,
                    is_staff=True,
                    is_superuser=False,
                    date_joined="2025-09-09T05:37:41.464443Z",
                    last_login="2025-09-09T05:37:41.464443Z"
                ),
                SimpleNamespace(
                    id=2,
                    username="user2",
                    email="user2@test.com",
                    is_active=True,
                    is_staff=True,
                    is_superuser=False,
                    date_joined="2025-09-09T05:37:41.464443Z",
                    last_login="2025-09-09T05:37:41.464443Z"
                ),
            ]
            all_mock.return_value = existing_users
            
            # Test function with mock data
            try:
                notify_via_email(
                    product_id,
                    product_name,
                    owner,
                    action
                )
            except Exception as e:
                all_mock.assert_called_once()
                send_email_mock.assert_not_called()
                assert str(e.args[0]) == "Sending email failed"
                assert isinstance(e.args[1], Exception)
        
    def test_send_email_smtp_fails(self):
        with patch("api.utils.email_utils.User.objects.all") as all_mock, \
            patch("api.utils.email_utils.send_mail", side_effect=Exception("smtp down")) as send_email_mock, \
            patch("api.utils.email_utils.EMAIL_HOST_USER", "noreply@test.com"):
            product_id = "123"
            product_name = "test_product"
            owner = "user@test.com"
            action = "MY_ACTION"
            existing_users = [
                SimpleNamespace(
                    id=1,
                    username="user",
                    email="user@test.com",
                    is_active=True,
                    is_staff=True,
                    is_superuser=False,
                    date_joined="2025-09-09T05:37:41.464443Z",
                    last_login="2025-09-09T05:37:41.464443Z"
                ),
                SimpleNamespace(
                    id=2,
                    username="user2",
                    email="user2@test.com",
                    is_active=True,
                    is_staff=True,
                    is_superuser=False,
                    date_joined="2025-09-09T05:37:41.464443Z",
                    last_login="2025-09-09T05:37:41.464443Z"
                ),
            ]
            all_mock.return_value = existing_users
            
            # Test function with mock data
            try:
                notify_via_email(
                    product_id,
                    product_name,
                    owner,
                    action
                )
            except Exception as e:
                send_email_mock.assert_called_once()
                send_email_mock.assert_called_once()
                assert str(e.args[0]) == "Sending email failed"
                assert isinstance(e.args[1], Exception)
        