from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag,Ingredient, Recipe

from recipe import serializers

class TagViewSet(viewsets.GenericViewSet, 
                mixins.ListModelMixin,
                mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class= serializers.TagSerializer

    def get_queryset(self):
        """Return object for current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """create a new tag with payload"""
        serializer.save(user=self.request.user)

class IngredintViewSet(viewsets.GenericViewSet, 
                mixins.ListModelMixin,
                mixins.CreateModelMixin):
    """manage our ingredients"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """create a new ingredient with payload"""
        serializer.save(user=self.request.user)

class RecipeViewset(viewsets.ModelViewSet):
    """manage recipes in the dataabase"""
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """return the needed serializer"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerialzer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
       """Create new recipe"""
       serializer.save(user=self.request.user)
