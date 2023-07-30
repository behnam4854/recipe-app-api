from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredient', views.IngredintViewSet)
router.register('recipes', views.RecipeViewset)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
