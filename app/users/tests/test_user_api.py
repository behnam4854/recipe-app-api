from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('users:create')

def create_user(**params):
    """this is helper function for our tests basicly we shorten the function that we already have with this"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """For test creating user"""
    def setUp(self):
        self.client = APIClient()

    def test_creating_user_success(self):
        """test for creating a valid user with valid data"""
        payload ={
            'email' : 'test55@test.com',
            'password' : 'te855st',
            'name' : 'behnam'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_if_the_user_already_exists(self):
        """check if the user is already signed up"""
        payload ={'email':'test@test.com', 'password': 'test'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test for creating user with short password"""  
        payload ={'email':'test@test.com', 'password': 'test'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(
                                email=payload['email']).exists()
        self.assertFalse(user_exist)




  