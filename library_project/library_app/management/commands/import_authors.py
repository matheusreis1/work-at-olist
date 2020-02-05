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
        self.stdout.write('Starting import authors')
        csv_file = options.get('csv_file')

        try:
            open(csv_file)
        except OSError:
            self.stderr.write("Could not open/read file: "+options.get('csv_file'))
            return

        with open(csv_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            headers = next(spamreader)
            for row in spamreader:
                name = row[0]
                Author.objects.create(
                  name=name
                )

        self.stdout.write('Done')
