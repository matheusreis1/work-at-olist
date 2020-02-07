from django.test import TestCase
from django.core import management
from rest_framework.test import APIClient
from library_app.models import Author
import json
import csv
from io import StringIO

# Create your tests here.
class ImportAuthorsTest(TestCase):
    def test_error_open_csv_file(self):
        """
            Test to verify name of file
        """
        out = StringIO()
        error_out = StringIO()
        management.call_command('import_authors', 'authors_error.csv', stdout=out,stderr=error_out)
        self.assertIn('Starting import authors', out.getvalue())
        self.assertIn('Could not open/read file: authors_error.csv', error_out.getvalue())

    def test_import_authors_csv_file(self):
        """
            Test import authors from csv file
        """
        out = StringIO()
        error_out = StringIO()
        management.call_command('import_authors', 'authors.csv', stdout=out, stderr=error_out)
        authors = Author.objects.all()

        with open('authors.csv') as csvfile:
            spamreader = csv.reader(csvfile)
            headers = next(spamreader)
            lines = list(spamreader)

        self.assertIn('Done', out.getvalue())
        self.assertEqual(authors.count(), len(lines))

    def test_error_import_authors_csv_file(self):
        """
            Test import authors from csv file
        """
        out = StringIO()
        error_out = StringIO()
        management.call_command('import_authors', 'library_app/tests/fixtures/authors_error.csv', stdout=out, stderr=error_out)
        self.assertIn('Error on document format.', error_out.getvalue())
