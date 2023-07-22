from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTest(TestCase):
    """For tests that doesnt require any authentication"""

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """test that user doesnt have access to others tags and it should be 401 authorized"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase):
    """for test that require authentication"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'behnam@test.com',
            'test1234pass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        """test for retriving tags"""
        Tag.objects.create(user=self.user, name='testtag1')
        Tag.objects.create(user=self.user, name='testtag2')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_auth_user(self):
        """test that tag is limited to authenticated user that no one but user can edit it"""
        user2 = get_user_model().objects.create_user(
            'behnam2@test.com',
            'test584545'
        )
        Tag.objects.create(user = user2, name = 'testtag')
        tag = Tag.objects.create(user = self.user, name = 'testtag2')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        
