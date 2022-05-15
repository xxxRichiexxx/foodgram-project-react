from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Tag


User = get_user_model()


class TagsTests(APITestCase):

    def setUp(self):
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
        self.expected_data_list = [
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
            "slug": "lunch",
            }
        ]

    def test_get_tags(self):
        """
        Получение списка тегов.
        """
        url = reverse('tags:tag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data_list)

    def test_get_tag(self):
        """
        Получение тега по id.
        """
        url = reverse('tags:tag-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data_list[0])