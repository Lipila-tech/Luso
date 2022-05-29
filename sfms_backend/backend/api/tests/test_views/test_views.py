
"""
This module contains unittests for the api app.
"""

from datetime import datetime
import django
from django.contrib.auth.models import User
from django.test import TestCase, Client
from api.models import Program
from api.models import Student
from api.models import Term
from api.models import Payment


class ViewsTestCase(TestCase):
    """Tests for the application views."""
    @classmethod
    def setUpTestData(cls):
        print('\n.................................')
        print('....... TESTING VIEWS .......')
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
        self.term1.save()

        # create programs
        self.program1 = Program.objects.create(
            program_name="Python Programming",
            tuition=4000)
        self.program1.save()

        self.program2 = Program.objects.create(
            program_name="Ruby Programming", tuition=4000)
        self.program2.save()

        self.program = Program.objects.get(id=1)

        # Create Students
        self.std1 = Student.objects.create(username=self.user0,
                                         tuition=2300, program=self.program)
        self.std1.save()
        self.std2 = Student.objects.create(username=self.user1,
                                         tuition=2300, program=self.program)
        self.std2.save()
        # Create payment
        self.payment = Payment.objects.create(amount=4000,
                                          pay_date="2022-05-10",
                                          student=self.std1, term=self.term1)

        # Send GET requests to API endpoints
        self.profile = Client().get("/api/v1/profile")
        self.payments = Client().get("/api/v1/payments?id=0")
        
        # POST payment
        s_id = self.std1.username_id
        s_id1 = self.std2.username_id
        t_id = self.term1.id     
               
        self.post_payment1 = Client().post("/api/v1/payments?id={}".format(s_id),
                                {"student": s_id,
                                 "amount": '2346',
                                 'mobile': '0971892260',
                                 'reference':'123456',
                                 "pay_date": "2021-05-10",
                                 "term": t_id})
        self.post_payment2 = Client().post("/api/v1/payments?id={}".format(s_id1),
                                {"student": s_id1,
                                 "amount": 3000,
                                 'mobile': '0971442260',
                                 'reference':'123457',
                                 "pay_date": "2021-05-10",
                                 "term": t_id})

        # POST payment with bad request
        self.post_payment3 = Client().post("/api/v1/payments?id=19",
                                {"amount":2346,
                                 "pay_date":"2022-05-10",
                                 "student": self.std2,
                                 "term": self.term1})
   
        # POST payment with bad request
        self.p5 = Client().post("/api/v1/payments?id={}".format(s_id),
                                {"amount":2346,
                                 "pay_date":"2022-05-10",
                                 "student": self.std2,
                                 "term": self.term1})
        # POST request to non existing route
        self.p6 = Client().post("/api/v1/not_a_view",
                                {"student": s_id,
                                 "amount": 2346,
                                 'mobile': '0971892260',
                                 'reference':'123456',
                                 "pay_date": "2021-05-10",
                                 "term": t_id})

    def test_login_success(self):
        """ TEST if login was succesful"""
        print('\n************************')
        print("******* Testing Login *******")
        print('\n')
        login = Client().login(username='pita', password='pwd_123')
        self.assertTrue(login)

    def test_logout_success(self):
        """test if session ended successfully"""
        print('\n************************')
        print("******* Testing Logout *******")
        print('\n')
        logout = Client().post("/api/v1/logout")
        self.assertTrue(logout)

    def test_wrong_credentials(self):
        print('\n************************')
        print("******* Testing Login unregistered user *******")
        print('\n')
        login = Client().login(username='pitaz', password='pwd_123')
        self.assertFalse(login)

    def test_valid_profile_route(self):
        """ GET valid terms route"""
        self.assertEqual(self.profile.status_code, 200)

    def test_payment_route(self):
        """ Test that API returns 404 if id not present""" 
        self.assertEqual(self.payments.status_code, 404)

    def test_invalid_route(self):
        """ GET invalid route """
        r1 = Client().get("/api/v1/not_a_view/")
        self.assertEqual(r1.status_code, 404)

    def test_post_response_201(self):
        """ POST payment data successfully to database"""
        print('\n************************')
        print("******* Testing POST requests on API *******")
        print('\n')
        self.assertEqual(self.post_payment1.status_code, 201)
        self.assertEqual(self.post_payment2.status_code, 201)

    def test_post_response_no_payment(self):
        """ Test post request with invalid message framing"""
        self.assertEqual(self.p5.status_code, 400)

    def test_post_response_404(self):
        """ Test post request with invalid message framing"""
        self.assertEqual(self.p6.status_code, 404)

    def test_invalid_student_id(self):
        """ Test that API returns 404 on invalid id""" 
        self.assertEqual(self.post_payment3.status_code, 404)

    def test_content_type(self):
        """ test content type of response"""
        self.assertEqual(self.profile['Content-Type'], "application/json")

    
        

    