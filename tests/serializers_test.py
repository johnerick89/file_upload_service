from django.test import TestCase
from api.models import User, File
from api.serializers import UserSerializer, FileSerializer

class UserSerializerTestCase(TestCase):
    def tearDown(self):
        self._fixture_teardown()

    def setUp(self):
        self.user_data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
        self.user = User.objects.create(**self.user_data)

    def test_valid_data(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        invalid_data = {'first_name': 'Jane', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_unique_email(self):
        data = {'first_name': 'Jane', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class FileSerializerTestCase(TestCase):
    def tearDown(self):
        self._fixture_teardown()

    def setUp(self):
        self.file_data = {'name': 'test_file', 'file': 'file_contents'}
        self.file = File.objects.create(**self.file_data)

    def test_valid_data(self):
        serializer = FileSerializer(data=self.file_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_name(self):
        invalid_data = {'file': 'file_contents'}
        serializer = FileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_missing_file(self):
        invalid_data = {'name': 'test_file'}
        serializer = FileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
