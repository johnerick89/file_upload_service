from django.urls import path
from api.views import FileUploadView, UserAPIView

urlpatterns = [
    path('upload', FileUploadView.as_view(), name='upload'),
    path('files', FileUploadView.as_view(), name='files'),
    path('users', UserAPIView.as_view(), name='users'),
]