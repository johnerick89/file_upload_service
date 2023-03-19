from django.test import TestCase
from api.models import File
from django.core.files.uploadedfile import SimpleUploadedFile


class FileModelTest(TestCase):
    def tearDown(self):
        self._fixture_teardown()
        
    def setUp(self):
        self.file = SimpleUploadedFile("file.txt", b"file_contents")
        self.file_obj = File.objects.create(file=self.file)

    def test_file_creation(self):
        """Test that a file is created with default status."""
        self.assertEqual(str(self.file_obj), "file.txt")
        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(self.file_obj.status, "new")

    def test_file_processing(self):
        """Test that a file is processed and status is changed to complete."""
        self.file_obj.status = "new"
        self.file_obj.save()
        self.assertEqual(self.file_obj.status, "processing")
        self.file_obj.refresh_from_db()
        self.assertEqual(self.file_obj.status, "complete")

    def test_file_processing_failure(self):
        """Test that a file processing failure changes the status to failed."""
        self.file_obj.status = "new"
        self.file_obj.save()
        self.assertEqual(self.file_obj.status, "processing")
        self.file_obj.refresh_from_db()
        self.assertEqual(self.file_obj.status, "failed")
