from django.test import TransactionTestCase
from datetime import date

from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import User
from api.serializers import UserSerializer, FileSerializer
from api.tasks import handle_uploaded_file_task


class UserSerializerTestCase(TransactionTestCase):
    def tearDown(self):
        self._fixture_teardown()

    def setUp(self):
        self.user_data = {
            'first_name': 'John', 
            'last_name': 'Doe', 
            'email': 'john.doe@test.com', 
            'national_id': "123456789",
            'birth_date': date(1990, 1, 1),
            'address': "123 Main St.",
            'country': "USA",'phone_number': "1234567890"}
        self.user = User.objects.create(**self.user_data)

    def test_valid_data(self):
        valid_data = {
            'first_name': 'John', 
            'last_name': 'Doe', 
            'email': 'john.doe@example.com', 
            'national_id': "123456789",
            'birth_date': date(1990, 1, 1),
            'address': "123 Main St.",
            'country': "USA",'phone_number': "1234567890"}
        serializer = UserSerializer(data=valid_data)
        
        self.assertTrue(serializer.is_valid())


    def test_invalid_email(self):
        invalid_data = {'first_name': 'Jane', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_unique_email(self):
        data = {'first_name': 'Jane', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class FileSerializerTestCase(TransactionTestCase):
    def tearDown(self):
        self._fixture_teardown()

    def test_valid_data(self):
        data = "John Smith 123456789 1990-01-01 123 Main St USA +1-123-456-7890 john.smith@example.com"
        file_data = SimpleUploadedFile("test_data.txt", data.encode())
        serializer = FileSerializer(data={'file': file_data})
        self.assertTrue(serializer.is_valid())

    def test_missing_file(self):
        invalid_data = {}
        serializer = FileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

