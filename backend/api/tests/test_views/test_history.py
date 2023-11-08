
"""
This module contains unittests for the api app's HistoryView.
"""

from datetime import datetime
from api.models import Payment
from api.models import Program
from api.models import Student
from api.models import Term

import django
from django.contrib.auth.models import User

from django.test import TestCase, Client




class HistoryTestCase(TestCase):
    """Tests for the application views."""
    @classmethod
    def setUpTestData(cls):
        print('\n.................................')
        print('....... TESTING HISTORY VIEW .......')
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

        # Create Terms
        start_d = datetime.strptime("2022-10-01", "%Y-%m-%d").date()
        end_d = datetime.strptime("2022-12-30", "%Y-%m-%d").date()
        self.term1 = Term.objects.create(name="Term1",
                                         start_date=start_d, end_date=end_d)


        # cretae programs
        self.program1 = Program.objects.create(
            program_name="Python Programming",
            tuition=4000)
        self.program2 = Program.objects.create(
            program_name="Ruby Programming", tuition=4000)

        self.program = Program.objects.get(id=1)


        # Create Students
        self.std1 = Student.objects.create(username=self.user0,
                                         tuition=2300, program=self.program)
        self.std2 = Student.objects.create(username=self.user1,
                                         tuition=2300, program=self.program)

        # Create payment
        self.payment = Payment.objects.create(amount=4000,
                                          pay_date="2022-05-10",
                                          student=self.std1, term=self.term1)

        # GET history
        student_id0 = self.std1.username_id  
        student_id1 = self.std2.username_id  
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



    
        

    