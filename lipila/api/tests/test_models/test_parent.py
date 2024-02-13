
"""
TESTS the Parent Model
"""

from django.contrib.auth.models import User
from django.test import TestCase
from api.models import Parent
from api.models import School
from datetime import datetime



class ParentTestCase(TestCase):
    """Tests for the application views."""
    def setUp(self):
        # Create User objects
        self.user1  = User.objects.create_user('Memo', 'memo@email.tech', 'memo@pswd')
        self.user2  = User.objects.create_user('Sepi', 'sepi@email.tech', 'sepi@pswd')

        # Create School objects
        self.school1 = School.objects.create(school_name="School1", administrator=self.user1)
        self.school1.save()

        self.school2 = School.objects.create(school_name="School2", administrator=self.user2)
        self.school2.save()
 
         # create Parent object
        self.parent1 = Parent.objects.create(
            first_name="first1", last_name="last1",
            school=self.school1)
        self.parent1.save() # save to db
        self.parent2 = Parent.objects.create(
            first_name="parent2", email_address="p2@bot.zm", mobile_number="888666555",
            school=self.school2)
        self.parent2.save() # save to db

    def test_parent_str_repr(self):
        self.assertEqual(str(self.parent1), "first1 last1")
        self.assertEqual(str(self.parent2), "parent2 ")

    def test_get_school_name_method(self):
        self.assertTrue(self.parent1.get_school_name(), "School1")
        self.assertTrue(self.parent2.get_school_name(), "School2")

    def test_contacts_method(self):
        self.assertEqual(self.parent1.get_contacts(), " ")
        self.assertEqual(self.parent2.get_contacts(), "p2@bot.zm 888666555")        
        


