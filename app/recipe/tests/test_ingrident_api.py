from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


ING_URL=reverse('recipe:ingredient-list')

class PublicIngredientApiTest(TestCase):
    """tests that can be accessed without authentication"""
    
    def setUp(self):
        self.client = APIClient()

    def test_getting_ingredient_witout_authentication(self):
        """test that the list shouldnt be accessed without authentication"""
        res = self.client.get(ING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientApiTest(TestCase):
    """test that require authentication"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email = 'behnam@test.com',
            name='behnam'
        )
        self.client.force_authenticate(self.user)
    
    def test_retriving_ings_list(self):
        """getting all the ingredient that user created"""
        Ingredient.objects.create(
            user=self.user,
            name = 'kaho'
        )
        Ingredient.objects.create(
            user=self.user,
            name='kalam'
        )
        res = self.client.get(ING_URL)
        ings = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ings, many=True)
        self.assertEqual(res.data,serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_limited_to_auth_user(self):
        """test that tag is limited to authenticated user that no one but user can edit it"""
        user2 = get_user_model().objects.create_user(
            'behnam2@test.com',
            'test584545'
        )
        Ingredient.objects.create(user = user2, name = 'khiyar')
        ings = Ingredient.objects.create(user = self.user, name = 'goje')

        res = self.client.get(ING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ings.name)

    def test_create_ingridient_successful(self):
        """test that we can create ingredient"""
        payload = {'name':'sir'}
        self.client.post(ING_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)
    
    def test_create_invalid_ingredient(self):
        """test that we cant create ingredient with invalid payload"""
        payload={'name':''}
        res = self.client.post(ING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        

