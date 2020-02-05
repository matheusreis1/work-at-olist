from django_filters import rest_framework as filters
from .models import Author, Book

class AuthorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Author
        fields = ['name',]

class BookFilter(filters.FilterSet):
    pass