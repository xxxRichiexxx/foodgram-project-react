from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AccountTests(APITestCase):

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
        self.expected_data_list = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "email": "test_user_1@mail.ru",
                    "id": 1,
                    "username": "test-user-1",
                    "first_name": "test_user",
                    "last_name": "test_user",
                    "is_subscribed": False
                },
                {
                    "email": "test_user_2@mail.ru",
                    "id": 2,
                    "username": "test-user-2",
                    "first_name": "test_user",
                    "last_name": "test_user",
                    "is_subscribed": False
                }
            ]
        }

    def test_create_user(self):
        """
        Регистрация пользователя.
        """
        url = "/api/users/"
        data = {
            "email": "test_user_3@mail.ru",
            "username": "test-user-3",
            "first_name": "test_user",
            "last_name": "test_user",
            "password": "qwerty_123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_get_token(self):
        """
        Получение токена.
        """
        url = reverse('auth&users:login')
        data = {
            "email": "test_user_1@mail.ru",
            "password": "qwerty_123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_token(self):
        """
        Удаление токена.
        """
        url = reverse('auth&users:logout')
        self.client.force_authenticate(self.test_user_one)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_users(self):
        """
        Получение списка пользователей.
        """
        url = reverse('auth&users:customuser-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data_list)

    def test_get_one_user_without_auth(self):
        """
        Получение детальной информации о пользователе по id.
        """
        url = reverse('auth&users:customuser-detail', args=[2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_one_user_with_auth(self):
        """
        Получение детальной информации о пользователе по id.
        """
        # url = reverse('auth&users:customuser-detail', args=[2])
        url = '/api/users/2/'
        self.client.force_authenticate(self.test_user_one)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data_list['results'][1])

    def test_get_me_with_auth(self):
        """
        Получение детальной информации о себе.
        """
        url = reverse('auth&users:customuser-detail', args=['me'])
        self.client.force_authenticate(self.test_user_two)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data_list['results'][1])

    def test_set_password(self):
        """
        Смена пароля.
        """
        url = reverse('auth&users:customuser-set-password')
        self.client.force_authenticate(self.test_user_one)
        data = {
            "new_password": "qwerty_456",
            "current_password": "qwerty_123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        url = reverse('auth&users:login')
        data = {
            "email": "test_user_1@mail.ru",
            "password": "qwerty_123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {
            "email": "test_user_1@mail.ru",
            "password": "qwerty_456",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
