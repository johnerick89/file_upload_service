from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from api.tasks import handle_uploaded_file_task

@patch('api.tasks.handle_uploaded_file')
def test_handle_uploaded_file_task(mock_handle_uploaded_file):
    # Define test data
    data = "John Smith 123456789 1990-01-01 123 Main St USA +1-123-456-7890 john.smith@example.com"
    txt_file = SimpleUploadedFile("test_data.txt", data.encode())

    # Call the task
    handle_uploaded_file_task.delay(txt_file)

    # Assert that the task was called with the correct arguments
    mock_handle_uploaded_file.assert_called_once_with(txt_file)
