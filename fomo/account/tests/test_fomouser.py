from django.test import TestCase
from account import import as amod

class AnimalTestCase(TestCase):
    # def setUp(self):
    #     Animal.objects.create(name="lion", sound="roar")
    #     Animal.objects.create(name="cat", sound="meow")

    def test_create_users(self):
        """Animals that can speak are correctly identified"""
        
