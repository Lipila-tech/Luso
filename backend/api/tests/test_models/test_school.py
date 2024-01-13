"""
TESTS THE School Model
"""

from django.contrib.auth.models import User
from django.test import TestCase
from api.models import School

class SchoolTestCase(TestCase):
    """Tests for the application views."""
    # Django requires an explicit setup() when running tests in PTVS
    def setUp(self):
        # Create User objects
        self.user1  = User.objects.create_user('Memo', 'memo@email.tech', 'memo@pswd')
        self.user2  = User.objects.create_user('Sepi', 'sepi@email.tech', 'sepi@pswd')

        # Create School objects
        self.school1 = School.objects.create(school_name="School1", administrator=self.user1)
        self.school1.save()

        self.school2 = School.objects.create(school_name="School1", administrator=self.user2)
        self.school2.save()

    def test_school_string_repr(self):
        """ Test string representation of the school"""
        self.assertEqual(str(self.school1), "School1")

    def test_school_creation(self):
        """ test the creation of a school"""
        self.assertEqual(School.objects.all().count(), 2)
        self.assertTrue(self.school1.id, 1)
        self.assertTrue(self.school2.pk, 2)



