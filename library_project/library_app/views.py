from django.shortcuts import render
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import AuthorFilter
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters

# Create your views here.
class AuthorAPI(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuthorFilter

class BookAPI(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name', 'publication_year', 'edition']
