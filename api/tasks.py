from celery import shared_task
from .upload_file_data import handle_uploaded_file

@shared_task()
def handle_uploaded_file_task(file):
    """Creates a task for handling the creation of the users data in the uploaded file."""
    handle_uploaded_file(file)