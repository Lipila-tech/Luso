"""
file: test_handler.py
This file contains tests for the 3rd Party API communication
in external_api_handler.py
"""


from django.test import TestCase, Client
from api.external_api_handler import APIHandler

class HandlerTestCase(TestCase):
    """Tests for the application views."""

    @classmethod
    def setUpTestData(cls):
        print('\n\n.................................')
        print('....... Testing External API.......')
        print('---------------------------------\n\n')

    def setUp(self):
        self.res = APIHandler()
        self.ref = self.res.get_uuid()
        self.user = self.res.create_api_user()
        self.key = self.res.get_api_key()
        self.token = self.res.get_api_token()
        self.payer0 = self.res.request_to_pay('36654', '0969620939', '56797356')
       
    # Django requires an explicit setup() when running tests in PTVS
    def test_x_reference_id(self):
        """ Test the x_reference id creation"""        
        self.assertEqual(self.ref.status_code, 200)

    def test_api_user(self):
        """ Test Sandbox user creation"""
        self.assertEqual(self.user.status_code, 201)

    def test_api_key(self):
        """Tesk Api key creaStion"""
        self.assertEqual(self.key.status_code, 201)

    def test_api_token(self):
        """ Test API access token creation"""
        self.assertEqual(self.token.status_code, 200)

    def test_request_to_pay(self):
        """Test request to pay method"""
        self.assertEqual(self.payer0.status_code, 202)

    def test_value_errors(self):
        """ Test the length of PartyId"""
        self.assertRaises(ValueError,
                          self.res.request_to_pay,
                          '36654', '096962', '56797356')
        self.assertRaises(ValueError,
                          self.res.request_to_pay,
                          '36654', '0969620978895774', '56797356')
        self.assertRaises(ValueError,
                          self.res.request_to_pay,
                          '50', '0969620978', '56797356')

    def test_type_errors(self):
        """Test the type of paramateres"""
        self.assertRaises(TypeError,
                          self.res.request_to_pay,
                          12345, '0969620939', '56797356')
        self.assertRaises(TypeError,
                          self.res.request_to_pay,
                          '12345', 969620939, '56797356')
        self.assertRaises(TypeError,
                          self.res.request_to_pay,
                          '12345', '0969620939', 56797356)
        



