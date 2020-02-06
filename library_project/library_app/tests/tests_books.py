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

        self.books = [
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

        self.setup_books(self.books)

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

    def test_search_exact_name(self):
        """
            Test of search book by exact name
        """
        name = self.books[0]['name']
        response = self.client.get(self.url+f"?name={name}")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Book.objects.all().filter(name=name).count())

    def test_search_contains_name(self):
        """
            Test of search book by part of name
        """
        response = self.client.get(self.url+"?name=Book")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, 4)

    def test_search_year(self):
        """
            Test of search book by publication year
        """
        publication_year = self.books[0]['publication_year']
        response = self.client.get(self.url+f"?publication_year={publication_year}")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Book.objects.all().filter(publication_year=publication_year).count())
    
    def test_search_edition(self):
        """
            Test of search book by edition
        """
        edition = self.books[0]['edition']
        response = self.client.get(self.url+f"?edition={edition}")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Book.objects.all().filter(edition=edition).count())
    
    def test_search_author(self):
        """
            Test of search book by author
        """
        pass
    
    def test_(self):
        pass
    
    def test_(self):
        pass
