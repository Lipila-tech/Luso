
"""
This module contains unittests for the api app's HistoryView.
"""

from datetime import datetime
from api.models import Payment
from api.models import Student
from api.models import Term

import django
from django.contrib.auth.models import User

from django.test import TestCase, Client




class HistoryTestCase(TestCase):
    """Tests for the application views."""
    @classmethod
    def setUpTestData(cls):
        print('\n.................................')
        print('....... TESTING HISTORY VIEW .......')
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

    
        

    