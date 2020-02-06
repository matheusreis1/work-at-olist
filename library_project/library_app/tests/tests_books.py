from django.test import TestCase
from rest_framework.test import APIClient
from library_app.models import Author, Book
from library_project.settings import REST_FRAMEWORK as drf_configs
import json
