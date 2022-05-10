
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import datetime
import django
from django.test import TestCase, Client
from ...models import Program
from ...models import Term
from ...models import Student
from ...models import Payment

# TODO: Configure your database in settings.py and sync before running tests.

class ViewsTestCase(TestCase):
    """Tests for the application views."""

    @classmethod
    def setUpTestData(cls):
        print('\n.................................')
        print('....... TESTING VIEWS .......')
        print('\n')

    def setUp(self):
        # Send GET requests to API endpoints
        self.response = Client().get("/api/v1/")
        self.r1 = Client().get("/api/v1/programs/")
        self.r2 = Client().get("/api/v1/terms/")
        self.r3 = Client().get("/api/v1/students/")
        self.r4 = Client().get("/api/v1/payments/")

        # Send POST requests
        # Create program
        self.p1 = Client().post("/api/v1/programs/",
                                {"program_name": "C# Tutorial",
                                 "tuition": 3400})
        # Create terms
        self.p2 = Client().post("/api/v1/terms/",
                                {"name":"term1", "start_date":"2022-08-01",
                                 "end_date":"2022-10-30"})
        # Create student
        self.p3 = Client().post("/api/v1/students/",
                                {"firstname":"Sangwani",
                                 "lastname":"zyambo",
                                 "tuition":"3000",
                                 "program": 1})
        # Create payment
        self.p4 = Client().post("/api/v1/payments/",
                                {"amount":2346,
                                 "pay_date":"2022-05-10",
                                 "student": 1,
                                 "term": 1})
        # Create payment with bad request
        self.p5 = Client().post("/api/v1/payments/",
                                {"amount":2346,
                                 "pay_date":"2022-05-10",
                                 "student": 1,
                                 "term": "term1"})
        # Post request to non existing route
        self.p6 = Client().post("/api/v1/not_a_view/",
                                {"program_name": "C# Tutorial",
                                 "tuition": 3400})
       
    def test_valid_api_route(self):
        """ Test if the payments api exists"""
        print('\n************************')
        print("******* Testing GET requests on API *******")
        print('\n')
        self.assertEqual(self.response.status_code, 200)

    def test_valid_programs_route(self):
        """ Test if programs route is valid"""
        program = Program.objects.create(program_name="Pascal Programming",
                                         tuition=4000)
        r2 = Client().get("/api/v1/programs/{}/".format(program.id))
        self.assertEqual(self.r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    def test_valid_terms_route(self):
        """ Test if terms route is valid"""
        start_d = datetime.strptime("2022-10-01", "%Y-%m-%d").date()
        end_d = datetime.strptime("2022-12-30", "%Y-%m-%d").date()
        # Create Terms
        term = Term.objects.create(name="Term1", start_date=start_d, end_date=end_d)
        r2 = Client().get("/api/v1/terms/{}/".format(term.id))
        self.assertEqual(self.r2.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    def test_valid_students_route(self):
        """ Test if students route is valid"""
        p = Program.objects.create(program_name="Ruby Programming",
                                         tuition=4000)
        
        # Create Students
        student = Student.objects.create(firstname="Memo", lastname="Zuze",
                                         tuition=2300, program=p)
        r2 = Client().get("/api/v1/students/{}/".format(student.student_no))
        self.assertEqual(self.r3.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    def test_valid_payment_route(self):
        """ Test if students route is valid"""
        program = Program.objects.create(
            program_name="Ruby Programming", tuition=4000)
        # Create student
        student = Student.objects.create(
            firstname="Sepiso", lastname="Muke",
            tuition=4000, program=program)
        # Create term
        term = Term.objects.create(name="Term1",
                                     start_date="2021-01-01",
                                     end_date="2021-04-01")
        # Create payment
        payment = Payment.objects.create(amount=4000,
                                          pay_date="2022-05-10",
                                          student=student, term=term)
        r2 = Client().get("/api/v1/payments/{}/".format(payment.id))
        self.assertEqual(self.r4.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    def test_invalid_route(self):
        """ Test get request on non existing route"""
        r1 = Client().get("/api/v1/not_a_view/")
        self.assertEqual(r1.status_code, 404)

    def test_post_response_201(self):
        """ Test if data was added successfully to db"""
        print('\n************************')
        print("******* Testing POST requests on API *******")
        print('\n')
        self.assertEqual(self.p1.status_code, 201)
        self.assertEqual(self.p2.status_code, 201)
        self.assertEqual(self.p3.status_code, 201)
        self.assertEqual(self.p4.status_code, 201)

    def test_post_response_400(self):
        """ Test post request with invalid message framing"""
        self.assertEqual(self.p5.status_code, 400)

    def test_post_response_404(self):
        """ Test post request with invalid message framing"""
        self.assertEqual(self.p6.status_code, 404)

    def test_content_type(self):
        """ test content type of response"""
        self.assertEqual(self.response['Content-Type'], "application/json")
        
    def test_put_on_program(self):
        print('\n************************')
        print("******* Testing PUT requests on API *******")
        print('\n')
        pass
        

    