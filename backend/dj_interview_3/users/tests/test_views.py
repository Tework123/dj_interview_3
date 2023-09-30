import datetime
from django.test import TestCase
from faker import Faker
from rest_framework import status
from users.models import CustomUser

fake = Faker()


class LoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """Заполняет данными базу"""
        CustomUser.objects.create_user(email='user1@mail.ru',
                                       password='user1@mail.ru')

        CustomUser.objects.create_user(email='user@mail.ru',
                                       password='user@mail.ru')

    def setUp(self) -> None:
        pass

    @staticmethod
    def get_user() -> CustomUser:
        """Возвращает тестового пользователя"""

        user = CustomUser.objects.get(email='user1@mail.ru')
        return user

    def auth_user(self) -> None:
        """Авторизуем пользователя"""
        self.client.login(email='user@mail.ru',
                          password='user@mail.ru')

    def test_user_create_already_exist(self):
        response = self.client.post('/users/',
                                    data={'email': 'user1@mail.ru',
                                          'password': '123123123'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create(self):
        response = self.client.post('/users/',
                                    data={'email': 'user2@mail.ru',
                                          'password': '123123123'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Пользователь успешно создан')

    def test_auth(self):
        response = self.client.post('/users/auth/',
                                    data={'email': 'user1@mail.ru',
                                          'password': 'user1@mail.ru'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Вход выполнен успешно')

    def test_users_list(self):
        response = self.client.get('/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_users_list_filter(self):
        self.auth_user()

        response = self.client.get('/users/filter/user@mail.ru/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['email'], 'user@mail.ru')

    def test_users_list_order_by(self):
        self.auth_user()

        response = self.client.get('/users/order_by/date_joined/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = CustomUser.objects.order_by('date_joined')
        self.assertEqual(len(response.data), len(order_data))
        self.assertEqual(response.data[0]['email'], order_data[0].email)

    def test_user_edit(self):
        self.auth_user()

        user = self.get_user()
        response = self.client.patch(f'/users/{user.pk}',
                                     data={
                                         'last_name': 'new_name',
                                         'date_of_birth': datetime.date.today()},
                                     content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Информация успешно обновлена')

        edit_user = CustomUser.objects.get(pk=user.pk)
        self.assertEqual(edit_user.last_name, 'new_name')

    def test_delete_account(self):
        self.auth_user()

        user = self.get_user()
        response = self.client.delete(f'/users/{user.pk}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Пользователь удален успешно')

        response = self.client.get(f'/users/{user.pk}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logout(self):
        self.auth_user()

        response = self.client.post('/users/logout/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Выход из аккаунта выполнен успешно')
