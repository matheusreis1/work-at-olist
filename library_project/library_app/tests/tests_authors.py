from django.test import TestCase
from rest_framework.test import APIClient
from library_app.models import Author
from library_project.settings import REST_FRAMEWORK as drf_configs
import json

# Create your tests here.
class AuthorApiTest(TestCase):

    authors = [
        {
            "name": "Luciano Ramalho"
        },
        {
            "name": "Osvaldo Santana Neto"
        },
        {
            "name": "David Beazley"
        },
        {
            "name": "Chetan Giridhar"
        },
        {
            "name": "Brian K. Jones"
        },
        {
            "name": "J.K Rowling"
        }
    ]

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/author/"
        authors = [Author(name=author['name']) for author in self.authors]
        Author.objects.bulk_create(authors)

    def test_get_method_status_code(self):
        """
            Test status code of GET method
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_count_get_authors(self):
        """
            Test count of authors in GET method
        """
        response = self.client.get(self.url)
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Author.objects.all().count())

    def test_get_author(self):
        """
            Test to get one author by id
        """
        name = self.authors[0]['name']
        author = Author.objects.get(name=name)
        response = self.client.get(self.url+f"{author.id}/")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['id'], author.id)

    def test_search_exact_name(self):
        """
            Test for search by exact name in authors GET method
        """
        name = self.authors[0]['name']
        response = self.client.get(self.url+f"?name={name}")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count , 1)

    def test_search_part_name(self):
        """
            Test for search by part of name in authors GET method
        """
        response = self.client.get(self.url+"?name=Lucian")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count , 1)

    def test_search_no_results_name(self):
        """
            Test for no results of name search
        """
        response = self.client.get(self.url+"?name=Matheus")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count , 0)

    def test_valid_page(self):
        """
            Test for valid page query
        """
        response = self.client.get(self.url+"?page=1")
        content = json.loads(response.content)
        count = content['count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Author.objects.all().count())

    def test_invalid_page(self):
        """
            Test for invalid page query
        """
        response = self.client.get(self.url+"?page=122")
        content = json.loads(response.content)
        detail = content['detail']
        self.assertEqual(response.status_code, 404)
        self.assertEqual(detail, "Invalid page.")

    def test_not_found_author(self):
        """
            Test for not found id in authors GET
        """
        response = self.client.get(self.url+"50/")
        content = json.loads(response.content)
        detail = content['detail']
        self.assertEqual(response.status_code, 404)
        self.assertEqual(detail, "Not found.")