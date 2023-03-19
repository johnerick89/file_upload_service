from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.views import status as http_status
from unittest.mock import MagicMock
from django.test import TransactionTestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from unittest.mock import MagicMock
from api.models import User, File
from api.views import UserAPIView, FileUploadView

from api.models import User, File
from api.serializers import UserSerializer, FileSerializer
from api.views import UserAPIView, FileUploadView


class UserAPIViewTestCase(TransactionTestCase):
    def tearDown(self):
        self._fixture_teardown()
        
    def setUp(self):
        self.user1 = User.objects.create(
            first_name='John',
            last_name='Doe',
            national_id='123456789',
            birth_date='1990-01-01',
            address='123 Main St',
            country='USA',
            phone_number='+1-123-456-7890',
            email='john.doe@example.com'
        )
        self.user2 = User.objects.create(
            first_name='Jane',
            last_name='Doe',
            national_id='987654321',
            birth_date='1979-01-01',
            address='456 Main St',
            country='Canada',
            phone_number='+1-987-654-3210',
            email='jane.doe@example.com'
        )

    def test_list_users(self):
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_users_by_first_name(self):
        url = reverse('users')
        response = self.client.get(url, {'first_name': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')

    def test_filter_users_by_country(self):
        url = reverse('users')
        response = self.client.get(url, {'country': 'Canada'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['country'], 'Canada')

    def test_order_users_by_last_name(self):
        url = reverse('users')
        response = self.client.get(url, {'ordering': 'last_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['last_name'], 'Doe')
        self.assertEqual(response.data[1]['last_name'], 'Doe')

    def test_filter_users_by_phone_number(self):
        url = reverse('users')
        response = self.client.get(url, {'phone_number': '+1-123-456-7890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')

    def test_filter_users_by_email(self):
        url = reverse('users')
        response = self.client.get(url, {'email': 'jane.doe@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Jane')


