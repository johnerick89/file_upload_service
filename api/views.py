from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework import status
from rest_framework import filters
import pandas as pd
from datetime import datetime

from .models import User, File
from .serializers import UserSerializer, FileSerializer
from .filters import UserFilter
from .upload_file_data import handle_uploaded_file
from .tasks import handle_uploaded_file_task

class UserAPIView(APIView):
    """
    List all users and allows for filtering of users
    """
    def get(self, request):
        users = User.objects.all()
        user_filter = UserFilter(request.query_params, queryset=users)
        filtered_queryset = user_filter.qs
        serializer = UserSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
    

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = UserFilter
    ordering_fields = ['first_name', 'last_name', 'birth_date', 'country', 'phone_number', 'email', 'national_id']


class FileUploadView(APIView):
    serializer_class = FileSerializer

    def _process_file(self, file_data):
        file_obj = File.objects.get(pk=file_data['id']) 
        file_obj.process_file()
        
        try:
            handle_uploaded_file_task.apply_async(args=[file_obj.file.path])
            file_obj.complete_processing()
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
            file_obj.fail_processing()
        
        file_obj.save()
        

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            allowed_file_types = ['.csv', '.xml', '.json', '.xls', '.txt', '.xlsx']
           
            if any(file.name.endswith(file_type) for file_type in allowed_file_types):
                serializer.save()
                self._process_file(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid file format. Only CSV files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request, format=None):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

