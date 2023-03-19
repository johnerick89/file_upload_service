from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import User
from datetime import date


class UserModelTest(TestCase):
    def tearDown(self):
        self._fixture_teardown()
        
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            national_id="123456789",
            birth_date=date(1990, 1, 1),
            address="123 Main St.",
            country="USA",
            phone_number="1234567890",
            email="john.doe@example.com"
        )

    def test_user_creation(self):
        """Test that a user is created with valid data."""
        self.assertEqual(str(self.user), "John Doe")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.finger_print_signature, self.user.get_finger_print_signature())

    def test_invalid_user_creation(self):
        """Test that a user cannot be created with invalid data."""
        invalid_user = User(first_name="", last_name="", national_id="", birth_date=None, address="", country="", phone_number="", email="")
        with self.assertRaises(ValidationError):
            invalid_user.full_clean()

    def test_finger_print_signature_generation(self):
        """Test that a finger print signature is generated on save."""
        self.user.finger_print_signature = ""
        self.user.save()
        self.assertIsNotNone(self.user.finger_print_signature)
