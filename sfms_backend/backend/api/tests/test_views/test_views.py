
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

from http.cookies import SimpleCookie

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
                                             email='test@example.com')
        self.user0.save()

        
        # Authenticate user0 and user0
        self.user0 = Client().login(username='memo', password='memo@pswd')
        self.user0 = Client().login(username='sepiso', password='sepiso@pswd')

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

        self.cookies = SimpleCookie()

        # Create Students
        self.s1 = Student.objects.create(username=self.user0,
                                         tuition=2300, program=self.program1)
        self.s2 = Student.objects.create(username=self.user0,
                                         tuition=2300, program=self.program2)

        # Create payment
        self.payment = Payment.objects.create(amount=4000,
                                          pay_date="2022-05-10",
                                          student=self.s1, term=self.term1)

        # Send GET requests to API endpoints
        self.response = Client().get("/api/v1/", )
        self.r1 = Client().get("/api/v1/programs/")
        self.r2 = Client().get("/api/v1/terms/")
        self.r3 = Client().get("/api/v1/students/")
        self.r4 = Client().get("/api/v1/payments/")

        # POST payment
        s_id = self.s2.username_id
        t_id = self.term1.id     
        self.post_payment1 = Client().post("/api/v1/payments/",
                                {"student": s_id,
                                 "amount": 2346,
                                 "pay_date": "2022-05-10",
                                 "term": t_id})
        self.post_payment2 = Client().post("/api/v1/payments/",
                                {"student": s_id,
                                 "amount": 3567,
                                 "pay_date": "2022-05-10",
                                 "term": t_id})
        # POST payment with bad request
        self.p5 = Client().post("/api/v1/payments/",
                                {"amount":2346,
                                 "pay_date":"2022-05-10",
                                 "student": self.s2,
                                 "term": self.term1})
        # POST request to non existing route
        self.p6 = Client().post("/api/v1/not_a_view/",
                                {"program_name": "C# Tutorial",
                                 "tuition": 3400})

    def test_login_success(self):
        """ TEST if login was succesful"""
        print('\n************************')
        print("******* Testing Login *******")
        print('\n')
        login = Client().login(username='pita', password='pwd_123')
        self.assertTrue(login)

    def test_wrong_credentials(self):
        print('\n************************')
        print("******* Testing Login unregistered user *******")
        print('\n')
        login = Client().login(username='pitaz', password='pwd_123')
        self.assertFalse(login)
       
    def test_valid_api_route(self):
        """ TEST if API ROUTE EXISTS"""
        print('\n************************')
        print("******* Testing GET requests on API *******")
        print('\n')
        self.assertEqual(self.response.status_code, 200)

    def test_valid_programs_route(self):
        """ GET vaild programs route"""
        r2 = Client().get("/api/v1/programs/{}/".format(self.program1.id))
        self.assertEqual(self.r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    def test_valid_terms_route(self):
        """ GET valid terms route"""
        r2 = Client().get("/api/v1/terms/{}/".format(self.term1.id))
        self.assertEqual(self.r2.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    def test_valid_students_route(self):
        """ GET valid students route"""        
        r2 = Client().get("/api/v1/students/{}/".format(self.s1.username_id))
        self.assertEqual(self.r3.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    def test_valid_payment_route(self):
        """ GET valid payments route""" 
        r2 = Client().get("/api/v1/payments/{}/".format(self.payment.student_id))
        self.assertEqual(self.r4.status_code, 200)
        self.assertEqual(r2.status_code, 200)

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
        self.assertEqual(self.response['Content-Type'], "application/json")
        
        

    