from django.urls import path
from api.views import FileUploadView, UserAPIView

urlpatterns = [
    path('upload', FileUploadView.as_view(), name='file-upload'),
    path('files', FileUploadView.as_view()),
    path('users', UserAPIView.as_view()),
]