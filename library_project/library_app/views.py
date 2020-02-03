from django.shortcuts import render
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import viewsets

# Create your views here.
class AuthorAPI(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer

class BookAPI(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')\
    serializer_class = BookSerializer
