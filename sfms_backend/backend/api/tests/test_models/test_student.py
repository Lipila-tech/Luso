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
        # Create User
        self.user1  = User.objects.create_user('Memo', 'memo@email.tech', 'memo@pswd')
        self.user2  = User.objects.create_user('Sepiso', 'sepiso@email.tech', 'sepiso@pswd')
        
        # Create Students
        self.s1 = Student.objects.create(username=self.user1,
                                         tuition=2300, program=self.p1)
        self.s2 = Student.objects.create(username=self.user2,
                                         tuition=4000, program=self.p2)

    def test_primary_keys_relation(self):
        """ Test if User id and Student have the same id"""
        self.assertEqual(self.user1.id, self.s1.username_id)
        self.assertEqual(self.user1.pk, self.s1.pk)

    def test_primary_keys(self):
        """ Test get_user_id method"""
        self.assertTrue(self.s1.get_user_id(), 1)
        self.assertTrue(self.s1.get_user_id(), 2)

    def test_username(self):
        """ tests get_username method"""
        self.assertTrue(self.s1.get_username, 'memo')
        self.assertTrue(self.s2.get_username, 'sepi')

    def test_tuition_fee(self):
        """ test the get_tuition method"""
        self.assertTrue(self.s1.get_tuition, 2300)
        self.assertTrue(self.s2.get_tuition, 4000)

    def test_student_str_repr(self):
        """ test the string representation"""
        self.assertEqual(str(self.s1), "memo")

    def test_correct_course(self):
        """ tests if the correct program was assigned to student"""
        sd1 = Student.objects.get(username_id=1)
        sd2 = Student.objects.get(username_id=2)
        self.assertEqual(str(sd1.program), "PASCAL PROGRAMMING")
        self.assertEqual(str(sd2.program), "RUBY PROGRAMMING")

    def test_related_names(self):
        """ Test the program related name on student"""
        self.assertTrue(self.p1.student, self.s1.program)
        self.assertTrue(self.p2.student, self.s2.program)

