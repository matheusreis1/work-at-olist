from django_filters import rest_framework as filters
from .models import Author, Book

class AuthorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Author
        fields = ['name',]

class BookFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    edition = filters.NumberFilter(field_name='edition')
    publication_year = filters.NumberFilter(field_name='publication_year')
    author = filters.ModelMultipleChoiceFilter(field_name='authors__name', to_field_name="name", queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ['name', 'edition', 'publication_year', 'author']
