from rest_framework import generics
from users.serializers import UserSerilizer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerilizer