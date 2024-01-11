
"""
This module contains unittests for the api app's HistoryView.
"""

from datetime import datetime
from api.models import Payment
from api.models import School
from api.models import Student
from api.models import Parent

import django
from django.contrib.auth.models import User

from django.test import TestCase, Client


class HistoryTestCase(TestCase):
    """Tests for the application views."""
    @classmethod
    def setUpTestData(cls):
        print('*******TESTING HISTORY VIEW******')
        print('\n')

    def setUp(self):
        # Create User
        self.user0 = User.objects.create_user(username='pita',
                                             password='pwd_123',
                                             email='pita@example.com')
        self.user0.save()

        self.user1 = User.objects.create_user(username='sepi',
                                             password='pwd_123',
                                             email='sepi@example.com')
        self.user1.save()

        # Create Schools
        self.school1 = School.objects.create(school_name="School1", administrator=self.user0)
        self.school1.save()

        # create parents
        self.parent1 = Parent.objects.create(
            first_name="Python Parentming",
            school=self.school1)
        self.parent1.save()

        self.parent2 = Parent.objects.create(
            first_name="Ruby Parentming", school=self.school1)
        self.parent2.save()

        self.parent = Parent.objects.get(id=1)

        # Create Students
        self.std1 = Student.objects.create(first_name="test firstname",
                                         parent_id=self.parent1, tuition=200.0, enrollment_number=123)
        self.std1.save()
        self.std2 = Student.objects.create(first_name="test firstname2",
                                         parent_id=self.parent2, tuition=12.1, enrollment_number=124)
        self.std2.save()
        # Create payment
        self.payment = Payment.objects.create(payment_amount=4000,
                                          payment_date="2022-05-10",
                                          enrollment_number=self.std1, school=self.school1)

        # GET history
        student_id0 = self.std1.id
        student_id1 = self.std2.id  
        self.get_history0 = Client().get("/api/v1/history?id={}".format(student_id0))
        self.get_history1 = Client().get("/api/v1/history?id={}".format(student_id1))
        self.get_history2 = Client().get("/api/v1/history?id=4")

    def test_get_history(self):
        """Test that API returns 200 code if data is present"""
        self.assertEqual(self.get_history0.status_code, 200)

    def test_get_history_no_payment(self):
        """Test that API returns 202 if data not available
        """
        self.assertEqual(self.get_history1.status_code, 204)

    def test_get_history_id_not_present(self):
        """Test that API returns 404 if user id not available
        """
        self.assertEqual(self.get_history2.status_code, 404)

    def test_content_type(self):
        """ test content type of response"""
        self.assertEqual(self.get_history0['Content-Type'], "application/json")
        self.assertEqual(self.get_history1['Content-Type'], "application/json")
        self.assertEqual(self.get_history2['Content-Type'], "application/json")



    
        

    