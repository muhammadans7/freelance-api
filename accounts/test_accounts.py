
from django.test import TestCase
from accounts.models import User
from accounts.services import signUp, login, get_user_byemail


class UserServiceTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
            "role": "client",
        }
        self.user, _ = signUp(**self.user_data)

    def test_signup_success(self):
        user, error = signUp("newuser", "new@example.com", "newpass", "freelancer")

        self.assertIsNotNone(user)
        self.assertIsNone(error)
        self.assertEqual(user.username, "newuser")

    def test_signup_duplicate_username(self):
        user, error = signUp("testuser", "another@example.com", "pass", "client")

        self.assertIsNone(user)
        self.assertEqual(error, "INVALID USERNAME")

    def test_signup_duplicate_email(self):
        user, error = signUp("anotheruser", "test@example.com", "pass", "client")

        self.assertIsNone(user)
        self.assertEqual(error, "INVALID EMAIL")

    def test_login_success(self):
        user, error = login("test@example.com", "securepassword123")

        self.assertIsNotNone(user)
        self.assertIsNone(error)
        self.assertEqual(user.username, "testuser")

    def test_login_invalid_email(self):
        user, error = login("wrong@example.com", "securepassword123")

        self.assertIsNone(user)
        self.assertEqual(error, "INVALID EMAIL")

    def test_login_invalid_password(self):
        user, error = login("test@example.com", "wrongpass")

        self.assertIsNone(user)
        self.assertEqual(error, "INVALID PASSWORD")

    def test_get_user_by_email_found(self):
        user = get_user_byemail("test@example.com")

        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_get_user_by_email_not_found(self):
        user = get_user_byemail("doesnotexist@example.com")

        self.assertIsNone(user)
