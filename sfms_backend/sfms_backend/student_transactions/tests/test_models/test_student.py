"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from ...models import Program
from ...models import Student


class TestStudentModels(TestCase):
    """Tests for the application views."""
    @classmethod
    def setUpTestData(cls):
        print('\n\n.................................')
        print('....... Testing Student class.......')
        print('---------------------------------\n\n')

    def setUp(self):
        # Create Programs
        self.p1 = Program.objects.create(program_name="Pascal Programming",
                                         tuition=4000)
        self.p2 = Program.objects.create(program_name="Ruby Programming",
                                         tuition=4000)
        
        # Create Students
        self.s1 = Student.objects.create(firstname="Memo", lastname="Zuze",
                                         tuition=2300, program=self.p1)
        self.s2 = Student.objects.create(firstname="Kapi", lastname="Zuze",
                                         tuition=2300, program=self.p2)

    def test_student_str_repr(self):
        """ test the string representation"""
        self.assertEqual(str(self.s1), "MEMO ZUZE")

    def test_correct_course(self):
        """ tests if the correct program was assigned to student"""
        sd1 = Student.objects.get(student_no=1)
        sd2 = Student.objects.get(student_no=2)
        self.assertEqual(str(sd1.program), "PASCAL PROGRAMMING")
        self.assertEqual(str(sd2.program), "RUBY PROGRAMMING")



