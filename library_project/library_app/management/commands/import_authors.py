from django.core.management.base import BaseCommand, CommandError
from library_app.models import Author
import csv

class Command(BaseCommand):
    """
        Import authors data from csv file to database
    """
    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    def handle(self, *args, **options):
        csv_file = options.get('csv_file')

        with open(csv_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                name = row[0]
                Author.objects.create(
                  name=name
                )