from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, data):
        """
            Validate values of publication year and edition in books api
        """
        publication_year = data.get("publication_year", None)
        edition = data.get("edition", None)
        messages = {}
        if publication_year and publication_year <= 0:
            messages['publication_year'] = "publication_year must be a positive integer."

        if edition and edition <= 0:
            messages['edition'] = "edition must be a positive integer."

        if messages:
            raise serializers.ValidationError(messages)
        return data
