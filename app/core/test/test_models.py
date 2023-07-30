from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='test@test.com', password='test123'):
    """sample user for testing purposes"""
    return get_user_model().objects.create_user(email, password)


class UserTests(TestCase):

    def test_create_user(self):
        """This is for testing if we can create a user currectly"""
        email = "behnam@gmail.com"
        password = "1234"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
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
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_tag_string(self):
        """if the tag is showing the string representaion"""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'test_tag'
        )
        self.assertEqual(str(tag),tag.name)

    def test_ingridient_string(self):
        """test if the string representation is currect"""
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = "test ingredient"
        )

        self.assertEqual(str(ingredient),ingredient.name)

    def test_recipe_str(self):
        """test that if it shows as we expected"""

        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title ='abghosht',
            time_minutes=50,
            price = 10000
        )

        self.assertEqual(str(recipe), recipe.title)