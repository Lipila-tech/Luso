
"""
TESTS the Payment Model
"""

from django.contrib.auth.models import User
from django.test import TestCase
from api.models import School
from api.models import Student
from api.models import Parent
from api.models import Payment

class PaymentTestCase(TestCase):
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
 
         # create Parent object
        self.parent1 = Parent.objects.create(
            first_name="Python Parentming",
            school=self.school1)
        self.parent1.save() # save to db
        self.parent2 = Parent.objects.create(
            first_name="Ruby Parentming", school=self.school1)
        self.parent2.save() # save to db

        # Create Student objects
        self.std1 = Student.objects.create(first_name="test firstname",
                                         parent_id=self.parent1, tuition=200.0, enrollment_number=123)
        self.std1.save() # save to db
        self.std2 = Student.objects.create(first_name="test firstname2",
                                         parent_id=self.parent2, tuition=12.1, enrollment_number=124)
        self.std2.save() # save to db        

        self.school_id = self.school1    
        self.school_id2 = self.school2    

        # Create Student payments
        self.pay1 = Payment.objects.create(enrollment_number=self.std1,
                                           payment_amount=4000,
                                           payment_method='0988774466',
                                           transaction_id='12345',
                                           payment_date="2022-05-10",
                                           description = "paid",
                                           school=self.school_id)
        self.pay2 = Payment.objects.create(enrollment_number=self.std1,
                                           payment_amount=4000,
                                           payment_method='0987654332',
                                           transaction_id='',
                                           payment_date="2022-05-10",
                                           description = "paid",
                                           school=self.school_id)
        self.pay3 = Payment.objects.create(enrollment_number=self.std2,
                                           payment_amount=3000,
                                           payment_method='0987645323',
                                           transaction_id='12345',
                                           payment_date="2022-05-10",
                                           description = "paid",
                                           school=self.school_id2)


    def test_get_enrollment_number_method(self):
        """ Test if Payment id and Student have the same id"""
        std_en = self.std1.get_enrollemnt_number()
        pay_en = self.pay1.get_enrollemnt_number()
        std2_en = self.std2.get_enrollemnt_number()
        pay2_en = self.pay3.get_enrollemnt_number()
        self.assertEqual(std_en, pay_en)
        self.assertEqual(std2_en, pay2_en)

    def test_payment_string_repr(self):
        """ Test string representation of the payment"""
        self.assertEqual(str(self.pay1), "1 4000 0988774466 12345 2022-05-10 School1 paid")
     
    def test_correct_students_payment(self):
        """ test if the correct student was given the payment"""
        self.assertTrue(self.pay1.payment_amount, 4000)
        self.assertTrue(self.pay3.payment_amount, 3000)



