from django.test import TestCase
from rest_framework.test import APIClient
from library_app.models import Author, Book
from library_project.settings import REST_FRAMEWORK as drf_configs
import json

# Create your tests here.
class BookApiTest(TestCase):

    authors = [
        {
            "name": "Luciano Ramalho"
        },
        {
            "name": "Osvaldo Santana Neto"
        }
    ]

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/book/"
        authors = [Author(name=author['name']) for author in self.authors]
        Author.objects.bulk_create(authors)

        books = [
            {
                "name": "Book 1",
                "edition": 1,
                "publication_year": 2020,
                "authors": [1, 2]
            },
            {
                "name": "Book 2",
                "edition": 1,
                "publication_year": 2019,
                "authors": [2]
            },
            {
                "name": "Book 2",
                "edition": 2,
                "publication_year": 2021,
                "authors": [2]
            },
            {
                "name": "Book 3",
                "edition": 1,
                "publication_year": 2020,
                "authors": [1]
            },
        ]

        self.setup_books(books)

    @staticmethod
    def setup_books(books):
        """
            Create books in database
        """
        for book in books:
            book_created = Book.objects.create(
                name = book['name'],
                edition = book['edition'],
                publication_year= book['publication_year']
            )
            book_created.authors.set(book['authors'])

    def test_get_books(self):
        """
            Test for status code in GET method
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # CRUD
    # Search by name, publication_year, edition, author

    def test_count_get_books(self):
        """
            Test of count of books in GET method
        """
        response = self.client.get(self.url)
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Book.objects.all().count())

    def test_search_name(self):
        pass

    def test_search_year(self):
        pass
    
    def test_search_edition(self):
        pass
    
    def test_search_author(self):
        pass
    
    def test_(self):
        pass
    
    def test_(self):
        pass
