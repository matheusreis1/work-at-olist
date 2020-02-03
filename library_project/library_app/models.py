from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    edition = models.FloatField()
    publication_year = models.FloatField()
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.name
