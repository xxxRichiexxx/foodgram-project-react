from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ingredient


class IngredientsTests(APITestCase):
    """Тесты для приложения Ингредиенты."""
    def setUp(self):
        self.ingredient_1 = Ingredient.objects.create(
            name="Ингредиент_1",
            measurement_unit="кг",
        )
        self.ingredient_2 = Ingredient.objects.create(
            name="Ингредиент_2",
            measurement_unit="кг",
        )
        self.expected_data = [
            {
                "id": 1,
                "name": "Ингредиент_1",
                "measurement_unit": "кг"
            },
            {
                "id": 2,
                "name": "Ингредиент_2",
                "measurement_unit": "кг"
            }
        ]

    def test_get_ingredients(self):
        """
        Получение списка ингредиентов.
        """
        url = reverse('ingredients:ingredient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data)

    def test_get_ingredient(self):
        """
        Получение ингредиента по id.
        """
        url = reverse('ingredients:ingredient-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data[0])
