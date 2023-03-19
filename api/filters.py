from django_filters import rest_framework as filters

from .models import User

class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    dob = filters.DateFromToRangeFilter()
    phone_number = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'dob', 'phone_number', 'email']