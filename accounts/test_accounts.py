from django.test import TestCase
from faker import Faker
from .models import User
from .services import (
    get_user_byemail,
    signup,
    login
)


# making an instance of faker
fake = Faker()

#  testing for model
class UserModelTest(TestCase):

    def test_user_creation(self):
        
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpassword123"))

    def test_default_role_is_user(self):
        
        user = User.objects.create_user(
            username="defaultroleuser", email="role@example.com", password="securepass"
        )
        
        self.assertEqual(user.role, "user")


class UserServiceTest(TestCase):
    
    def setUp(self):
        self.username = fake.user_name()
        self.email = fake.email()
        self.password = fake.password()
        self.role = "freelancer"
        

    def test_signup_success(self):
        
        user , error = signup(
            username=self.username,
            email=self.email,
            password=self.password,
            role=self.role
        )
        
        self.assertIsNotNone(user)
        self.assertIsNone(error)
        self.assertEqual(user.email , self.email)


    def test_signup_existing_username(self):
        
        User.objects.create_user(
            username=self.username,
            email=fake.email(),
            password=self.password,
            role=self.role,
        )
        
        user, error = signup(
            username=self.username,
            email=self.email,
            password=self.password,
            role=self.role,
        )
        self.assertIsNone(user)
        self.assertEqual(error, "INVALID USERNAME")

    def test_signup_existing_email(self):
        User.objects.create_user(
            username=fake.user_name(),
            email=self.email,
            password=self.password,
            role=self.role,
        )
        user, error = signup(
            username=self.username,
            email=self.email,
            password=self.password,
            role=self.role,
        )
        self.assertIsNone(user)
        self.assertEqual(error, "INVALID EMAIL")

    def test_get_user_by_email_success(self):
        user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            role=self.role,
        )
        found_user = get_user_byemail(self.email)
        self.assertEqual(found_user.id, user.id)

    def test_get_user_by_email_invalid(self):
        found_user = get_user_byemail("nonexistent@example.com")
        self.assertIsNone(found_user)

    def test_login_success(self):
        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            role=self.role,
        )
        user, error = login(email=self.email, password=self.password)
        self.assertIsNotNone(user)
        self.assertIsNone(error)

    def test_login_invalid_email(self):
        user, error = login(email="fake@email.com", password="pass123")
        self.assertIsNone(user)
        self.assertEqual(error, "INVALID EMAIL")

    def test_login_invalid_password(self):
        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            role=self.role,
        )
        user, error = login(email=self.email, password="wrongpassword")
        self.assertIsNone(user)
        self.assertEqual(error, "INVALID PASSWORD")
