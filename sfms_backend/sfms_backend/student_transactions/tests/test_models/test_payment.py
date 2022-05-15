
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.contrib.auth.models import User
from django.test import TestCase
from student_transactions.models import Program
from student_transactions.models import Student
from student_transactions.models import Term
from student_transactions.models import Payment
from datetime import datetime

class PaymentTestCase(TestCase):
    """Tests for the application views."""

    @classmethod
    def setUpTestData(cls):
        print('\n\n.................................')
        print('....... Testing Payment class.......')
        print('---------------------------------\n\n')

    # Django requires an explicit setup() when running tests in PTVS
    def setUp(self):
        # Create programs
        self.pro1 = Program.objects.create(
            program_name="Pascal Programming", tuition=4000)
        self.pro2 = Program.objects.create(
            program_name="Ruby Programming", tuition=4000)

        # Create User
        self.user1  = User.objects.create_user('Memo', 'memo@email.tech', 'memo@pswd')
        # Create student
        self.std = Student.objects.create(
            username=self.user1,
            tuition=4000,
            program=self.pro1)
        # Create term
        self.t = Term.objects.create(name="Term1",
                                     start_date="2021-01-01",
                                     end_date="2021-04-01")
        # Create payment
        self.pay = Payment.objects.create(amount=4000,
                                          pay_date="2022-05-10",
                                          student=self.std, term=self.t)

    def test_payment_string_repr(self):
        """ Test string representation of the payment"""
        self.assertEqual(str(self.pay), "Amount: 4000 Student Info: memo")
     
    def test_correct_students_payment(self):
        """ test if the correct student was given the payment"""
        self.assertEqual(self.std.id, self.pay.student.id)




