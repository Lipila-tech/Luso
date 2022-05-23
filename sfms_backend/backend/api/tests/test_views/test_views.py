
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


        # cretae programs
        self.program1 = Program.objects.create(
            program_name="Python Programming",
            tuition=4000)
        self.program2 = Program.objects.create(
            program_name="Ruby Programming", tuition=4000)

        self.program = Program.objects.get(id=1)

        #self.cookies = SimpleCookie()

        # Create Students
        self.std1 = Student.objects.create(username=self.user0,
                                         tuition=2300, program=self.program)
        self.std2 = Student.objects.create(username=self.user1,
                                         tuition=2300, program=self.program)

        # Create payment
        self.payment = Payment.objects.create(amount=4000,
                                          pay_date="2022-05-10",
                                          student=self.std1, term=self.term1)

        # Send GET requests to API endpoints
        self.profile = Client().get("/api/v1/profile")
        self.payments = Client().get("/api/v1/payments")
        
        # POST payment
        s_id = self.std2.username_id
        t_id = self.term1.id     
        self.post_payment1 = Client().post("/api/v1/payments?partyId=0969620939&externalId=88478",
                                {"student": s_id,
                                 "amount": 2346,
                                 "pay_date": "2021-05-10",
                                 "term": t_id})
        self.post_payment2 = Client().post("/api/v1/payments?partyId=0969620939&externalId=88478",
                                {"student": s_id,
                                 "amount": 3567,
                                 "pay_date": "2022-05-10",
                                 "term": t_id})
   
        # POST payment with bad request
        self.p5 = Client().post("/api/v1/payments?partyId=0969620939&externalId=88478",
                                {"amount":2346,
                                 "pay_date":"2022-05-10",
                                 "student": self.std2,
                                 "term": self.term1})
        # POST request to non existing route
        self.p6 = Client().post("/api/v1/not_a_view",
                                {"program_name": "C# Tutorial",
                                 "tuition": 3400})

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

    def test_valid_payment_route(self):
        """ GET valid payments route""" 
        self.assertEqual(self.payments.status_code, 200)

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

    def test_post_response_400(self):
        """ Test post request with invalid message framing"""
        self.assertEqual(self.p5.status_code, 400)

    def test_post_response_404(self):
        """ Test post request with invalid message framing"""
        self.assertEqual(self.p6.status_code, 404)

    def test_content_type(self):
        """ test content type of response"""
        self.assertEqual(self.profile['Content-Type'], "application/json")

    
        

    