from django.test import TestCase
from rest_framework.test import APIClient
from library_app.models import Author, Book
from library_app.serializers import AuthorSerializer, BookSerializer
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

    def test_count_get_books(self):
        """
            Test of count of books in GET method
        """
        response = self.client.get(self.url)
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Book.objects.all().count())

    def test_post_right_book(self):
        """
            Test to create a book with right fields and values
        """
        json_book = {
            "name": "Book Test",
            "edition": 1,
            "publication_year": 2020,
            "authors": [1]
        }
        response = self.client.post(self.url, data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in content.keys())
        self.assertTrue(content['name'] == json_book['name'])
        self.assertTrue(content['edition'] == json_book['edition'])
        self.assertTrue(content['publication_year'] == json_book['publication_year'])
        self.assertTrue(content['authors'] == json_book['authors'])

    def test_post_book_negative_edition(self):
        """
            Test create a book with right fields and
            negative value in edition
        """
        json_book = {
            "name": "Book Test",
            "edition": -1,
            "publication_year": 2020,
            "authors": [1]
        }
        response = self.client.post(self.url, data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['edition'], ["edition must be a positive integer."])

    def test_post_book_negative_year(self):
        """
            Test create a book with right fields and
            negative value in publication year
        """
        json_book = {
            "name": "Book Test",
            "edition": 1,
            "publication_year": -2020,
            "authors": [1]
        }
        response = self.client.post(self.url, data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['publication_year'], ["publication_year must be a positive integer."])

    def test_post_book_negative_edition_and_year(self):
        """
            Test to create a book with right fields and 
            negative values in edition and publication year
        """
        json_book = {
            "name": "Book Test",
            "edition": -1,
            "publication_year": -2020,
            "authors": [1]
        }
        response = self.client.post(self.url, data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['publication_year'], ["publication_year must be a positive integer."])
        self.assertEqual(content['edition'], ["edition must be a positive integer."])

    def test_create_book_without_name(self):
        """
            Test creation of book without name
        """
        json_book = {
            "name": "",
            "edition": 1,
            "publication_year": 2020,
            "authors": [1]
        }
        response = self.client.post(self.url, data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['name'], ["This field may not be blank."])

    def test_create_book_without_edition(self):
        """
            Test creation of book without edition
        """
        json_book = {
            "name": "Book test",
            "edition": "",
            "publication_year": 2020,
            "authors": [1]
        }
        response = self.client.post(self.url, data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['edition'], ["A valid integer is required."])

    def test_create_book_without_year(self):
        """
            Test creation of book without publication year
        """
        json_book = {
            "name": "Book test",
            "edition": 1,
            "publication_year": "",
            "authors": [1]
        }
        response = self.client.post(self.url, data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['publication_year'], ["A valid integer is required."])

    def test_create_book_without_authors(self):
        """
            Test creation of book without authors list
        """
        json_book = {
            "name": "Book test",
            "edition": 1,
            "publication_year": 2020,
            "authors": []
        }
        response = self.client.post(self.url, data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['authors'], ["This list may not be empty."])

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
        author = self.authors[0]['name']
        response = self.client.get(self.url+f"?author={author}")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)

    def test_put_book(self):
        """
            Test to update book's fields
        """
        json_book = {
            "name": "Book 11",
            "edition": 2,
            "publication_year": 2021,
            "authors": [1, 2]
        }
        response = self.client.put(self.url+"1/", data=json_book)
        content = json.loads(response.content)
        book_db = Book.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, BookSerializer(book_db).data)

    def test_put_book_negative_edition(self):
        """
            Test to update book with a negative edition
        """
        json_book = {
            "name": "Book 11",
            "edition": -2,
            "publication_year": 2021,
            "authors": [1, 2]
        }
        response = self.client.put(self.url+"1/", data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['edition'], ["edition must be a positive integer."])

    def test_put_book_negative_year(self):
        """
            Test to update book with a negative publication year
        """
        json_book = {
            "name": "Book 11",
            "edition": -2,
            "publication_year": -2021,
            "authors": [1, 2]
        }
        response = self.client.put(self.url+"1/", data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['edition'], ["edition must be a positive integer."])
        self.assertEqual(content['publication_year'], ["publication_year must be a positive integer."])

    def test_put_book_negative_year_and_edition(self):
        """
            Test to update book with negative publication year
            and edition
        """
        json_book = {
            "name": "Book 11",
            "edition": -2,
            "publication_year": -2021,
            "authors": [1, 2]
        }
        response = self.client.put(self.url+"1/", data=json_book)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['publication_year'], ["publication_year must be a positive integer."])

    def test_delete_book(self):
        """
            Test to delete a book
        """
        response = self.client.delete(self.url+"1/")
        self.assertEqual(response.status_code, 204)
        response_get = self.client.get(self.url+"1/")
        content = json.loads(response_get.content)
        self.assertEqual(response_get.status_code, 404)
        self.assertEqual(content, {"detail": "Not found."})