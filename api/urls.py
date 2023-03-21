from django.urls import path
from api.views import FileUploadView, UserAPIView

urlpatterns = [
    path('file_uploads', FileUploadView.as_view(), name='file_uploads'),
    path('users', UserAPIView.as_view(), name='users'),
]