from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse('recipe:recipe-list')

def sample_recipe(user, **params):
    """simple recipe that we can use or update later on"""
    defaults = {
        'title' : 'abgosht',
        'time_minutes' : 10,
        'price' : 2000
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)

class PublicRecipeApiTest(TestCase):
    """for testing recipe without authentication"""

    def setUp(self):
        self.client = APIClient()
    
    def test_getting_list_without_auth(self):
        """test getting the list of recipe without authentication"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """for testing recipe with authenticated user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email = 'behnam58584@gmail.com',
            password = 'testpassword'
        )
        self.client.force_authenticate(self.user)
    
    def test_getting_list_recipe(self):
        """test getting all the recipe with auth user"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_recipe_limited_to_user(self):
        """test that auth user have access to its own recipes"""
        user2 = get_user_model().objects.create_user(
            email = 'testuser@test.com',
            password = 'testpassword1235'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)