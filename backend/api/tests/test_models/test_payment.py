
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.contrib.auth.models import User
from django.test import TestCase
from api.models import Program
from api.models import Student
from api.models import Term
from api.models import Payment
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
        self.user2  = User.objects.create_user('Sepi', 'sepi@email.tech', 'sepi@pswd')

        # Create student
        self.std1 = Student.objects.create(
            username=self.user1,
            tuition=4000,
            program=self.pro1)

        self.std2 = Student.objects.create(
            username=self.user2,
            tuition=4690,
            program=self.pro2)

        # Create term
        self.t = Term.objects.create(name="Term1",
                                     start_date="2021-01-01",
                                     end_date="2021-04-01")
        # Create Student payments
        self.pay1 = Payment.objects.create(student=self.std1,
                                           amount=4000,
                                           mobile='0988774466',
                                           reference='12345',
                                           pay_date="2022-05-10",
                                           term=self.t)
        self.pay2 = Payment.objects.create(student=self.std1,
                                           amount=4000,
                                           mobile='0987654332',
                                           reference='',
                                           pay_date="2022-05-10",
                                           term=self.t)
        self.pay3 = Payment.objects.create(student=self.std2,
                                           amount=3000,
                                           mobile='0987645323',
                                           reference='12345',
                                           pay_date="2022-05-10",
                                           term=self.t)


    def test_student_payment_relationship(self):
        """ Test if Payment id and Student have the same id"""
        self.assertEqual(self.std1.username_id, self.pay1.student_id)
        self.assertEqual(self.std1.pk, self.pay2.student_id)
        self.assertEqual(self.std2.pk, self.pay3.student_id)

    def test_payment_string_repr(self):
        """ Test string representation of the payment"""
        self.assertEqual(str(self.pay1), "memo 4000 0988774466 12345 2022-05-10 Term1 2021-04-01")
     
    def test_correct_students_payment(self):
        """ test if the correct student was given the payment"""
        self.assertTrue(self.std1.username_id, self.pay1.student.username_id)
        self.assertTrue(self.std2.username_id, self.pay3.student.username_id)

    def test_correct_additional_payment(self):
        """ Test if subsequent payment are assigned to correct student"""
        self.assertTrue(self.std1.username_id, self.pay2.student.username_id)

    def test_related_names(self):
        """ Test the student related name on payment"""
        self.assertTrue(self.std1.payment, self.pay1.student_id)
        self.assertTrue(self.t.id, self.pay1.term)




