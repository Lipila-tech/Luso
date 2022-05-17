
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from student_transactions.models import Term
from datetime import datetime



class TermTestCase(TestCase):
    """Tests for the application views."""
    @classmethod
    def setUpTestData(cls):
        print('\n\n.................................')
        print('....... Testing Term class.......')
        print('---------------------------------\n\n')

    def setUp(self):
        # Create Dates
        start_d1 = datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        end_d1 = datetime.strptime("2022-04-04", "%Y-%m-%d").date()
        start_d2 = datetime.strptime("2022-05-01", "%Y-%m-%d").date()
        end_d2 = datetime.strptime("2022-08-30", "%Y-%m-%d").date()
        start_d3 = datetime.strptime("2022-10-01", "%Y-%m-%d").date()
        end_d3 = datetime.strptime("2022-12-30", "%Y-%m-%d").date()
        # Create Terms
        self.t1 = Term.objects.create(name="Term1", start_date=start_d1, end_date=end_d1)
        self.t2 = Term.objects.create(name="Term2", start_date=start_d2, end_date=end_d2)
        self.t3 = Term.objects.create(name="Term3", start_date=start_d3, end_date=end_d2)

    def test_term_str_repr(self):
        """ test string representation"""
        self.assertEqual(str(self.t1), "Term1 2022-04-04")

    def test_valid_term_period(self):
        """ test if a term period is valid"""
        self.assertTrue(self.t1.is_valid_term())

    def test_invalid_term_period(self):
        """ tests if the term dates are invalid"""
        self.assertFalse(self.t3.is_valid_term())
        
        


