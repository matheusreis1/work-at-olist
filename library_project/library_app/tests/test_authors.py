from django.test import TestCase
from rest_framework.test import APIClient
from library_app.models import Author

# Create your tests here.
class AuthorApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/author/"

    def test_get_method_status_code(self):
        """
            Testing status code of GET method
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_teste(self):
        self.assertTrue(True)