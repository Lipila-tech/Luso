
"""
Test the MTN Views
"""
from django.contrib.auth.models import User
from django.test import TestCase, Client
from api.models import School
from api.models import Student
from api.models import Parent
from api.models import Payment, LipilaPayment

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


class LipilaCollectionViewTest(APITestCase):

    def test_get_payments(self):
        """Tests retrieving a list of payments."""
        url = reverse('lipila-payment-list')  # Generate URL using basename
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)  # Assert successful response
        self.assertIsInstance(response.data, list)  # Assert data is a list

    def test_create_payment(self):
        """Tests creating a payment with date deserialization."""
        data1 =  {
           "amount" : 100,
            "description":"test description",
            "payer_account":"8855994499",
            "payer_name":"test payer name",
            "payer_email":"test@bot.com",
            "receiver_account":"9988557733",
            "status":'success',
        }
        data2 =  {
            "amount" : 400,
            "description":"test description",
            "payer_account":"8855994499",
            "payer_name":"test payer name",
            "payer_email":"test@bot.com",
            "receiver_account":"9988557733",
            "status":'pending',
        }
        url = reverse('lipila-payment-list')
        response = self.client.post(url, data1)
        
        self.assertEqual(response.status_code, 202)  # Assert successful creation
        self.assertEqual(response.headers['Content-Type'] , 'application/json')  # Assert successful creation
        
        self.assertEqual(LipilaPayment.objects.count(), 1)
        T1 = LipilaPayment.objects.get(id=1) # get first object
        self.assertEqual(T1.amount, 100)        
        self.assertEqual(T1.status, 'success') #assert success

        response = self.client.post(url, data2) # make second payment
        self.assertEqual(LipilaPayment.objects.count(), 2) # assert successful creation
        T2 = LipilaPayment.objects.get(id=2) # get second object
        self.assertEqual(T2.amount, 400)
        self.assertEqual(T2.status, 'success') #assert success
        self.assertNotEqual(T1.reference_id, T2.reference_id) # assert unique reference_id


class ViewsTestCaseGet(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ViewsTestCaseGet, cls).setUpClass()
    # def setUp(self):
        # Endpoints
        cls.payment_url = '/lipila/api/v1/payment/'
        cls.school_url = '/lipila/api/v1/school/'
        cls.student_url = '/lipila/api/v1/student/'
        cls.parent_url = '/lipila/api/v1/parent/'
        cls.profile_url = '/lipila/api/v1/profile/'

    # TEST GET REQUESTS
    def test_invalid_route(self):
        """ GET invalid route """
        r1 = Client().get("/lipila/api/v1/not_a_view/")
        self.assertEqual(r1.status_code, 404)

    def test_get_response_200(self):
        get_payment = Client().get(ViewsTestCaseGet.payment_url)
        get_parent = Client().get(self.parent_url)
        get_school = Client().get(self.school_url)
        get_student = Client().get(self.student_url)
        get_profile = Client().get(self.profile_url)

        self.assertEqual(get_payment.status_code, 200)
        self.assertEqual(get_parent.status_code, 200)
        self.assertEqual(get_school.status_code, 200)
        self.assertEqual(get_student.status_code, 200)
        self.assertEqual(get_profile.status_code, 200)

class ViewsTestCasePost(TestCase):
    """Tests for the application views."""
    def setUp(self):
        # Endpoints
        self.payment_url = '/lipila/api/v1/payment/'
        self.school_url = '/lipila/api/v1/school/'
        self.student_url = '/lipila/api/v1/student/'
        self.parent_url = '/lipila/api/v1/parent/'
        self.profile_url = '/lipila/api/v1/profile/'

        # Create User objects
        self.user0 = User.objects.create_user(username='pita',
                                             password='pwd_123',
                                             email='pita@example.com')
        self.user0.save() # save to db
        self.user1 = User.objects.create_user(username='sepi',
                                             password='pwd_123',
                                             email='sepi@example.com')
        self.user1.save() # save to db

        # Create School objects
        self.school1 = School.objects.create(school_name="School1", administrator=self.user0)
        self.school1.save()

        # create Parent object
        self.parent1 = Parent.objects.create(
            first_name="Python Parentming",
            school=self.school1)
        self.parent1.save() # save to db
        self.parent2 = Parent.objects.create(
            first_name="Ruby Parentming", school=self.school1)
        self.parent2.save() # save to db

        # Create Students objects
        self.std1 = Student.objects.create(first_name="test firstname",
                                         parent_id=self.parent1, tuition=200.0, enrollment_number=123)
        self.std1.save() # save to db
        self.std2 = Student.objects.create(first_name="test firstname2",
                                         parent_id=self.parent2, tuition=12.1, enrollment_number=124)
        self.std2.save() # save to db
                
        # Get the school and student ids
        student1_id = self.std1.id
        school_id = self.school1.id     
        
        # Valid data
        self.data1 =  {
            "enrollment_number": student1_id,
            "payment_amount": '2346',
            "payment_method": '0971892260',
            "transaction_id":'123456',
            "payment_date": "2021-05-10",
            "description": "paid",
            "school": school_id
            }
        # Arguments missing required field
        self.data2 =  {
            "payment_amount": '2346',
            "payment_method": '0971892260',
            "transaction_id":'123456',
            "payment_date": "2021-05-10",
            "description": "paid",
            "school": school_id
            }
        # Arguments with wring field type
        self.data3 =  {
            "enrollment_number": 'STRINGID',
            "payment_amount": '2346',
            "payment_method": '0971892260',
            "transaction_id":'123456',
            "payment_date": "2021-05-10",
            "description": "paid",
            "school": school_id
            }
        
        # Valid post
        self.post_payment1 = Client().post(self.payment_url, self.data1, format="json")
        # POST payment with bad data
        self.post_payment2 = Client().post(self.payment_url, self.data2)
   
        # POST request with invalid enrollment_number type
        self.post_payment3 = Client().post(self.payment_url, self.data3)

    # TEST AUTH
    def test_login_success(self):
        """ TEST if login was succesful"""
        login = Client().login(username='pita', password='pwd_123')
        self.assertTrue(login)

    def test_logout_success(self):
        """test if session ended successfully"""
        logout = Client().post("/lipila/api/v1/logout")
        self.assertTrue(logout)

    def test_wrong_credentials(self):
        login = Client().login(username='pitaz', password='pwd_123')
        self.assertFalse(login)

    # TEST POST REQUESTS
    def test_post_response_201(self):
        """ valid post request"""
        self.assertEqual(self.post_payment1.status_code, 201)
        self.assertEqual(Payment.objects.count(), 1)  # Verify payment was created in database
        post_payment = Client().post(self.payment_url, self.data1)
        self.assertEqual(post_payment.status_code, 201)
        self.assertEqual(Payment.objects.count(), 2)  # Verify payment was created in database

    def test_post_response_bad_data_400(self):
        """ invalid data arguments"""
        self.assertEqual(self.post_payment3.status_code, 400)

    def test_invalid_studenschool_id_400(self):
        """ invalid data type""" 
        self.assertEqual(self.post_payment2.status_code, 400)