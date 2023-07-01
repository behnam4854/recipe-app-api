from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTests(TestCase):

    def test_create_user(self):
        """This is for testing if we can create a user currectly"""
        email = "behnam@gmail.com"
        password = "1234"

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_if_the_email_is_normal(self):
        """check if the entered email is normilzed and all lower case"""
        email = "behnam@tEst.Com"
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_user_creation_with_no_email(self):
        """If the user want to create with no email must raise a value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
    
    def test_create_new_superuser(self):
        """For creating new superuser"""
        email = "behnam@gmail.com"
        password = "1234"

        user = get_user_model().objects.create_superuser(
            email = email,
            password = password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
