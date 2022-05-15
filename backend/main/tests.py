from PIL import Image
from io import BytesIO

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.base import File

from .models import Recipe, Ingredient, RecipeIngredients
from tags.models import Tag


User = get_user_model()


class RecipesTests(APITestCase):

    def setUp(self):
        self.test_user_one = User.objects.create_user(
            username='test-user-1',
            first_name='test_user',
            last_name='test_user',
            email='test_user_1@mail.ru',
            password='qwerty_123',
        )
        self.test_user_two = User.objects.create_user(
            username='test-user-2',
            first_name='test_user',
            last_name='test_user',
            email='test_user_2@mail.ru',
            password='qwerty_123',
        )
        self.tag_1 = Tag.objects.create(
            name = "Завтрак",
            color = "#E26C2D",
            slug = "breakfast",
        )
        self.tag_2 = Tag.objects.create(
            name = "Обед",
            color = "#E26C2A",
            slug = "lunch",
        )
        self.ingredient_1 = Ingredient.objects.create(
            name = "Ингредиент_1",
            measurement_unit = "кг",
        )
        self.ingredient_2 = Ingredient.objects.create(
            name = "Ингредиент_2",
            measurement_unit = "кг",
        )
        file_obj = BytesIO()
        image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
        image.save(file_obj, 'png')
        file_obj.seek(0)
        self.recipe_1 = Recipe.objects.create(
            name = "рецепт_1",
            text = "рецепт_1",
            cooking_time = 2,
            author_id = self.test_user_one,
            image = File(file_obj, name='image')
        )
        self.recipe_1.tags.add(self.tag_1, self.tag_2)
        RecipeIngredients.objects.create(
            recipe_id = self.recipe_1,
            ingredient_id = self.ingredient_1,
            amount = 20,          
        )
        RecipeIngredients.objects.create(
            recipe_id = self.recipe_1,
            ingredient_id = self.ingredient_2,
            amount = 20,          
        )
        self.expected_data_list = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
                    {
                    "id": 1,
                    "tags": [
                            {
                            "id": 1,
                            "name": "Завтрак",
                            "color": "#E26C2D",
                            "slug": "breakfast"
                            },
                            {
                            "id": 2,
                            "name": "Обед",
                            "color": "#E26C2A",
                            "slug": "lunch"
                            }                            
                    ],
                    "author": {
                                "email": 'test_user_1@mail.ru',
                                "id": 1,
                                "username": 'test-user-1',
                                "first_name": 'test_user',
                                "last_name": 'test_user',
                                "is_subscribed": False
                    },
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "рецепт_1",
                    "text": "рецепт_1",
                    "cooking_time": 2
                    }
        ]
        }

    def test_get_recipes(self):
        """
        Получение списка рецептов.
        """
        url = reverse('recipes:recipe-list')
        response = self.client.get(url)
        image = response.data['results'][0].pop('image')
        self.assertNotEqual(image, None)
        date = response.data['results'][0].pop('date')
        self.assertNotEqual(date, None)
        ingredients = response.data['results'][0].pop('ingredients')
        self.assertNotEqual(ingredients, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data_list)

    def test_get_recipe(self):
        """
        Получение рецепта по id.
        """
        url = reverse('recipes:recipe-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        image = response.data.pop('image')
        self.assertNotEqual(image, None)
        date = response.data.pop('date')
        self.assertNotEqual(date, None)
        ingredients = response.data.pop('ingredients')
        self.assertNotEqual(ingredients, None)
        self.assertEqual(response.data, self.expected_data_list['results'][0])

    def test_create_recipe(self):
        """
        Создание рецепта.
        """
        url = '/api/recipes/'
        data = {
            "ingredients": [
                {
                "id": 1,
                "amount": 10
                }
            ],
            "tags": [
                1,
                2
            ],
            "image": """data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEA
                        AAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACX
                        BIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOy
                        YQAAAABJRU5ErkJggg==""",
            "name": "test_recipe",
            "text": "test_recipe",
            "cooking_time": 2
        }
        self.client.force_authenticate(self.test_user_one)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)

    def test_del_recipe_auth(self):
        """
        Удаление рецепта по id(автор).
        """
        url = '/api/recipes/1/'
        self.client.force_authenticate(self.test_user_one)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_del_recipe_no_auth(self):
        """
        Удаление рецепта по id(не автор).
        """
        url = '/api/recipes/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(self.test_user_two)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_download_shopping_cart(self):
        """
        Получение списка покупок.
        """
        url = reverse('recipes:recipe-download-shopping-cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(self.test_user_one)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_del_to_shopping_cart(self):
        """
        Добавление рецепта к списку покупок, удаление. 
        """
        url = reverse('recipes:recipe-shopping-cart', args=[1])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(self.test_user_one)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_user_one.shopping_list.count(), 1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_user_one.shopping_list.count(), 0)

    def test_add_del_to_favorite(self):
        """
        Добавление рецепта в избранное, удаление. 
        """
        url = reverse('recipes:recipe-favorite', args=[1])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(self.test_user_one)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_user_one.favorite_recipes.count(), 1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_user_one.favorite_recipes.count(), 0)     

    def test_add_del_to_subscriptions(self):
        """
        Добавление автора в подписки, удаление. 
        """
        url = reverse('auth&users:customuser-subscribe', args=[2])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(self.test_user_one)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_user_one.authors.count(), 1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_user_one.authors.count(), 0)  

    def test_get_subscriptions(self):
        """
        Просмотр подписок. 
        """
        url = reverse('auth&users:customuser-subscriptions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        url = reverse('auth&users:customuser-subscribe', args=[1])
        self.client.force_authenticate(self.test_user_two)
        self.client.post(url)
        url = reverse('auth&users:customuser-subscriptions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data_list={
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
                    {
                    "first_name": "test_user",
                    "last_name": "test_user",
                    "username": "test-user-1",
                    "id": 1,
                    "email": "test_user_1@mail.ru",                                       
                    "is_subscribed": True,
                    "recipes": [
                                {
                                "id": 1,
                                "name": "рецепт_1",
                                "cooking_time": 2
                                }
                    ],
                    "recipes_count": 1
                    }
        ]
        }
        image = response.data['results'][0]['recipes'][0].pop('image')
        self.assertNotEqual(image, None)
        self.assertEqual(response.data, expected_data_list)