from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django_fsm import FSMIntegerField, transition
from .models import User, File

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'