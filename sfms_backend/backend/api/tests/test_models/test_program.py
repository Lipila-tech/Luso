"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from api.models import Program

class ProgramTestCase(TestCase):
    """Tests for the application views."""

    @classmethod
    def setUpTestData(cls):
        print('\n\n.................................')
        print('....... Testing Program class.......')
        print('---------------------------------\n\n')

    # Django requires an explicit setup() when running tests in PTVS
    def setUp(self):
        # Create Programs
        self.p1 = Program.objects.create(program_name="Pascal Programming",
                                         tuition=4000)
        self.p2 = Program.objects.create(program_name="Ruby Programming",
                                         tuition=4000)
        self.p3 = Program.objects.create(program_name="Lua Programming",
                                         tuition=4000)

    def test_program_string_repr(self):
        """ Test string representation of the program"""
        self.assertEqual(str(self.p1), "PASCAL PROGRAMMING")

    def test_program_creation(self):
        """ test the creation of a program"""
        self.assertEqual(Program.objects.all().count(), 3)
        self.assertTrue(self.p1.id, 1)
        self.assertTrue(self.p3.id, 3)



