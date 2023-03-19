from django.utils import timezone
from django.test import TestCase
from django.test import TransactionTestCase
from django_filters import rest_framework as filters
from mixer.backend.django import mixer

from api.models import User
from api.filters import UserFilter

class UserFilterTestCase(TransactionTestCase):
    def tearDown(self):
        self._fixture_teardown()

    def setUp(self):
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.dob = timezone.now().date()
        self.phone_number = '+11234567890'
        self.email = 'johndoe@example.com'

        # Create test users
        self.user1 = mixer.blend(User, first_name=self.first_name, last_name=self.last_name, birth_date=self.dob, phone_number=self.phone_number, email=self.email)
        self.user2 = mixer.blend(User, first_name='Jane', last_name='Doe', birth_date=self.dob, phone_number='+1234567890', email='janedoe@example.com')

    def test_filter_by_first_name(self):
        data = {'first_name': self.first_name}
        queryset = User.objects.all()
        f = UserFilter(data, queryset=queryset)

        self.assertEqual(len(f.qs), 1)
        self.assertEqual(f.qs[0], self.user1)

    def test_filter_by_dob(self):
        data = {'dob_after': self.dob - timezone.timedelta(days=1), 'dob_before': self.dob + timezone.timedelta(days=1)}
        queryset = User.objects.all()
        f = UserFilter(data, queryset=queryset)

        self.assertEqual(len(f.qs), 2)

    def test_filter_by_phone_number(self):
        data = {'phone_number': self.phone_number}
        queryset = User.objects.all()
        f = UserFilter(data, queryset=queryset)

        self.assertEqual(len(f.qs), 1)
        self.assertEqual(f.qs[0], self.user1)

    def test_filter_by_email(self):
        data = {'email': self.email}
        queryset = User.objects.all()
        f = UserFilter(data, queryset=queryset)

        self.assertEqual(len(f.qs), 1)
        self.assertEqual(f.qs[0], self.user1)
