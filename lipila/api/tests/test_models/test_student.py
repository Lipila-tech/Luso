"""
TEST the Student Model
"""

from django.contrib.auth.models import User
from django.test import TestCase
from api.models import School
from api.models import Student
from api.models import Parent


class TestStudentModels(TestCase):
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
            first_name="parent2", email_address="p1@bot.zm", mobile_number="888777555",
            school=self.school1)
        self.parent1.save() # save to db
        self.parent2 = Parent.objects.create(
            first_name="parent2", email_address="p2@bot.zm", mobile_number="888666555",
            school=self.school2)
        self.parent2.save() # save to db

        # Create Student objects
        self.std1 = Student.objects.create(first_name="first1", last_name="last1",
                                         parent_id=self.parent1, tuition=200.0, enrollment_number=123)
        self.std1.save() # save to db
        self.std2 = Student.objects.create(first_name="first2", last_name="last2",
                                         parent_id=self.parent2, tuition=120.1, enrollment_number=124)
        self.std2.save() # save to db  

    def test_get_school_name_method(self):
        self.assertEqual(self.std1.get_school_name(), "School1")
        self.assertEqual(self.std2.get_school_name(), "School2")

    def test_get_parent_email_method(self):
        self.assertEqual(self.std1.get_parent_email(), "p1@bot.zm")
        self.assertEqual(self.std2.get_parent_email(), "p2@bot.zm")

    def test_get_parent_phone_method(self):
        self.assertEqual(self.std1.get_parent_phone(), "888777555")
        self.assertEqual(self.std2.get_parent_phone(), "888666555")

    def test_get_enrollment_numebr_method(self):
        """ Test get_user_id method"""
        self.assertTrue(self.std1.get_enrollemnt_number(), 123)
        self.assertTrue(self.std2.get_enrollemnt_number(), 124)

    def test_tuition_fee(self):
        """ test the get_tuition method"""
        self.assertTrue(self.std1.get_tuition(), 200.0)
        self.assertTrue(self.std1.get_tuition(), 120.1)

    def test_student_str_repr(self):
        """ test the string representation"""
        self.assertEqual(str(self.std1), "123 first1 last1 200.0 School1")
        self.assertEqual(str(self.std2), "124 first2 last2 120.1 School2")

    def test_get_student_names_method(self):
        std1 = Student.objects.get(id=1)
        std2 = Student.objects.get(id=2)
        self.assertEqual(std1.get_student_names(), "first1 last1")
        self.assertEqual(std2.get_student_names(), "first2 last2")

    def test_school_admin_id(self):
        """ check school admin"""
        self.assertTrue(self.school1.administrator.id, self.user1.id)
        self.assertTrue(self.school2.administrator.id, self.user2.id)

