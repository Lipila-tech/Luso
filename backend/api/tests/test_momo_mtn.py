"""
Tests the mtn momo API
"""


from django.test import TestCase, Client
from api.momo.mtn import Collections, Disbursement
from api.helpers import get_uuid4


class MTNBaseTestCase(TestCase):
    """ Tests inheritance """

    def setUp(self):
        self.col_mtn = Collections()
        self.dis_mtn = Disbursement()

    def test_collections_inheritance(self):
        self.assertTrue(self.col_mtn.x_target_environment, 'sandbox')
        self.assertTrue(len(self.col_mtn.subscription_col_key), 32)
        self.assertEqual(self.col_mtn.content_type, 'application/json')
        # assert different instances
        self.assertNotEqual(self.col_mtn.x_reference_id,
                            self.dis_mtn.x_reference_id)

    def test_disbursement_inheritance(self):
        self.assertTrue(self.dis_mtn.x_target_environment, 'sandbox')
        self.assertTrue(len(self.dis_mtn.subscription_dis_key), 32)
        self.assertEqual(self.dis_mtn.content_type, 'application/json')
        self.assertNotEqual(self.col_mtn.x_reference_id,
                            self.dis_mtn.x_reference_id)

    def test_sandbox_provisioning_collection(self):
        self.assertEqual(self.col_mtn.api_key, '')
        self.assertEqual(self.col_mtn.api_token, 'Bearer ')
        ref_id = self.col_mtn.provision_sandbox(
            self.col_mtn.subscription_col_key)
        self.assertEqual(ref_id.status_code, 201)  # 3 assert methods success
        self.assertNotEqual(ref_id, '')
        self.assertNotEqual(ref_id, 'Bearer ')
        token = self.col_mtn.create_api_token(
            self.col_mtn.subscription_col_key, 'collection')
        self.assertEqual(token.status_code, 200)


    def test_sandbox_provisioning_disbursement(self):
        self.assertEqual(self.dis_mtn.api_key, '')
        self.assertEqual(self.dis_mtn.api_token, 'Bearer ')
        ref_id = self.dis_mtn.provision_sandbox(
            self.dis_mtn.subscription_dis_key)
        self.assertEqual(ref_id.status_code, 201)  # 3 assert methods success
        self.assertNotEqual(ref_id, '')
        self.assertNotEqual(ref_id, 'Bearer ')
        token = self.dis_mtn.create_api_token(
            self.dis_mtn.subscription_dis_key, 'disbursement')
        self.assertEqual(token.status_code, 200)


class MTNCollectionsTestCase(TestCase):
    """Test MTN Collections methods"""

    def setUp(self):
        self.momo = Collections()
        self.ref = get_uuid4()
        self.user = self.momo.create_api_user(self.momo.subscription_col_key)
        self.key = self.momo.create_api_key(self.momo.subscription_col_key)
        self.token = self.momo.create_api_token(
            self.momo.subscription_col_key, 'collection')
        self.payer0 = self.momo.request_to_pay('2456', '0969620939', 'myrefre')

    def test_x_reference_id(self):
        """ Test the x_reference id creation"""
        self.assertEqual(type(self.ref), str)

    def test_api_user(self):
        """ Test Sandbox user creation"""
        self.assertEqual(self.user.status_code, 201)

    def test_api_key(self):
        """Tesk Api key creaStion"""
        self.assertEqual(self.key.status_code, 201)

    def test_api_token(self):
        """ Test API access token creation"""
        self.assertEqual(self.token.status_code, 200)

    def test_request_to_pay_accepted(self):
        """Test request to pay method"""
        self.assertEqual(self.payer0.status_code,
                         202)  # assert successful accepted

    def test_get_payment_status_completed(self):
        """Test get payment status method"""
        get_payment_status = self.momo.get_payment_status()  # check the payment status
        # assert completed successfullys
        self.assertEqual(get_payment_status.status_code, 200)

    def test_validate_collection_account_holder(self):
        """validate collections account"""
        check_account_status = self.momo.validate_account_holder(
            self.momo.subscription_col_key, 'msisdn', '0965766634', 'collection')
        self.assertEqual(check_account_status.status_code,
                         200)  # assert successful

    def test_raise_value_errors(self):
        """ Test the length of PartyId"""
        self.assertRaises(ValueError,
                          self.momo.request_to_pay,
                          '36654', '096962', '56797356')
        self.assertRaises(ValueError,
                          self.momo.request_to_pay,
                          '36654', '0969620978895774', '56797356')
        self.assertRaises(ValueError,
                          self.momo.request_to_pay,
                          '5', '0969620978', '56797356')

    def test_raise_type_errors(self):
        """Test the type of paramateres"""
        self.assertRaises(TypeError,
                          self.momo.request_to_pay,
                          12345, '0969620939', '56797356')
        self.assertRaises(TypeError,
                          self.momo.request_to_pay,
                          '12345', 969620939, '56797356')
        self.assertRaises(TypeError,
                          self.momo.request_to_pay,
                          '12345', '0969620939', 56797356)


class MTNDisbursementTestCase(TestCase):
    """Test MTN Disbursement methods"""

    def setUp(self):
        self.momo = Disbursement()
        self.ref = get_uuid4()
        self.user = self.momo.create_api_user(self.momo.subscription_dis_key)
        self.key = self.momo.create_api_key(self.momo.subscription_dis_key)
        self.token = self.momo.create_api_token(
            self.momo.subscription_dis_key, 'disbursement')
        self.deposit = self.momo.deposit('3665', '0969620939', 'therence')

    def test_api_user(self):
        """ Test Sandbox user creation"""
        self.assertEqual(self.user.status_code, 201)

    def test_api_key(self):
        """Tesk Api key creaStion"""
        self.assertEqual(self.key.status_code, 201)

    def test_api_token(self):
        """ Test API access token creation"""
        self.assertEqual(self.token.status_code, 200)

    def test_validate_disbursement_account_holder(self):
        """validate disbursement account"""
        check_account_status = self.momo.validate_account_holder(
            self.momo.subscription_dis_key, 'msisdn', '0966776644', 'disbursement')
        self.assertEqual(check_account_status.status_code,
                         200)  # assert successful

    def test_deposit_accepted(self):
        """Test the deposit method"""
        self.assertEqual(self.deposit.status_code,
                         202)  # assert successful accepted

    def test_get_deposit_status_completed(self):
        """Test get transer status method"""
        get_deposit_status = self.momo.get_transaction_status(
            'deposit', self.momo.x_reference_id)  # check the payment status
        # assert completed successfullys
        self.assertEqual(get_deposit_status.status_code, 200)

    def test_raise_value_errors(self):
        """ Test the length of PartyId"""
        self.assertRaises(ValueError,
                          self.momo.deposit,
                          '36654', '096962', '56797356')
        self.assertRaises(ValueError,
                          self.momo.deposit,
                          '36654', '0969620978895774', '56797356')
        self.assertRaises(ValueError,
                          self.momo.deposit,
                          '5', '0969620978', '56797356')

    def test_raise_type_errors(self):
        """Test the type of paramateres"""
        self.assertRaises(TypeError,
                          self.momo.deposit,
                          12345, '0969620939', '56797356')
        self.assertRaises(TypeError,
                          self.momo.deposit,
                          '12345', 969620939, '56797356')
        self.assertRaises(TypeError,
                          self.momo.deposit,
                          '12345', '0969620939', 56797356)
