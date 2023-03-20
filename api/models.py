from django.db import models
from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_by, fsm_log_description
import hashlib
import uuid

from .upload_file_data import handle_uploaded_file
from .tasks import handle_uploaded_file_task



class User(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    national_id = models.CharField(max_length=255, null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    country = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    finger_print_signature = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.finger_print_signature:
            unique_value = str(uuid.uuid4())
            hashed_value = hashlib.sha256(unique_value.encode()).hexdigest()
            self.finger_print_signature = hashed_value
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'users'


class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    status = FSMField(default='new', protected=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(File, self).save(*args, **kwargs)
        if self.status == 'new':
            self.process_file()

    class Meta:
        db_table = 'files'
    
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='new', target='processing')
    def process_file(self):
        try:
            # handle_uploaded_file(self.file)
            # Spawn a new Celery task for processing the file data
            handle_uploaded_file_task.apply_async(args=[self.file.path])
            self.complete_processing()
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
            self.fail_processing()
    
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source=['new','processing'], target='complete')
    def complete_processing(self):
        return 'Status is complete'
    

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source=['new','processing'], target='failed')
    def fail_processing(self):
        return 'Status is failed'
        
        