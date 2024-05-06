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
        # Create a first momo collection user instance
        self.momo1 = Collections()
        self.ref = get_uuid4()
        self.api_user = self.momo1.create_api_user(
            self.momo1.subscription_col_key)
        self.api_key = self.momo1.create_api_key(
            self.momo1.subscription_col_key)
        self.api_token = self.momo1.create_api_token(
            self.momo1.subscription_col_key, 'collection')

    def test_x_reference_id(self):
        """ Test the x_reference id creation"""
        self.assertEqual(type(self.ref), str)

    def test_api_user(self):
        """ Test Sandbox user creation"""
        self.assertEqual(self.api_user.status_code, 201)

    def test_api_key(self):
        """Tesk Api key creation"""
        self.assertEqual(self.api_key.status_code, 201)

    def test_api_token(self):
        """ Test API access token creation"""
        self.assertEqual(self.api_token.status_code, 200)

    def test_request_to_pay_accepted(self):
        """Returns 202 accepted status"""
        momo2 = Collections()
        api_user = momo2.create_api_user(
            momo2.subscription_col_key)
        api_key = momo2.create_api_key(
            momo2.subscription_col_key)
        api_token = momo2.create_api_token(
            momo2.subscription_col_key, 'collection')
        payment = self.momo1.request_to_pay('2456', '0969620939', 'myrefre')
        self.assertEqual(payment.status_code, 202)
        self.assertEqual(payment.data['message'], 'pending')
        # duplicate request to pay
        payment = self.momo1.request_to_pay('56', '0969610939', 'newrefere')
        self.assertEqual(payment.status_code, 409)
        self.assertEqual(payment.data['reason'], 'Conflict user exists')
        # new collection object request
        payment = momo2.request_to_pay('56', '0969610939', 'newrefere')
        self.assertEqual(payment.status_code, 202)
        self.assertEqual(payment.data['message'], 'pending')       

    def test_request_to_pay_bad_request(self):
        """Returns 400 bad request status"""
        with self.assertRaises(ValueError) as rtp:
            self.momo1.request_to_pay('6', '0969620939', 'myrefre')
        self.assertEqual(str(
            rtp.exception), 'Amount must be greater than 10 and partyid must be 10 digits long.')

        with self.assertRaises(ValueError) as rtp:
            payment = self.momo1.request_to_pay('2456', '9620939', 'myrefre')
        self.assertEqual(str(
            rtp.exception), 'Amount must be greater than 10 and partyid must be 10 digits long.')
        # reference should not have spaces
        with self.assertRaises(ValueError) as rtp:
            payment = self.momo1.request_to_pay(
                '2456', '9620939545', 'my refre')
        self.assertEqual(str(rtp.exception),
                         "Reference should not contain spaces.")

    def test_get_payment_status_completed(self):
        """Returns a 200 OK status"""
        payment = self.momo1.request_to_pay('2456', '0969620939', 'myrefre')
        get_payment_status = self.momo1.get_payment_status(
            self.momo1.x_reference_id)
        # assert completed successfully ok
        self.assertEqual(get_payment_status.status_code, 200)

    def test_get_payment_status_bad_request(self):
        """Returns a 400 bad request status"""
        get_payment_status = self.momo1.get_payment_status(
            '8647749439037hhfkgsdhfkla67e839')
        # assert completed successfully with error
        self.assertEqual(get_payment_status.data['reason'], 'Bad Request')
        self.assertEqual(get_payment_status.status_code, 400)

    def test_get_payment_status_404(self):
        """Returns a 404 user not found status code"""
        momo2 = Collections()
        get_payment_status = self.momo1.get_payment_status(
            momo2.x_reference_id)
        self.assertEqual(get_payment_status.status_code, 404)
        self.assertEqual(get_payment_status.data['reason'], 'Not Found')

    def test_validate_collection_account_holder(self):
        """validate collections account"""
        check_account_status = self.momo1.validate_account_holder(
            self.momo1.subscription_col_key, 'msisdn', '0965766634', 'collection')
        self.assertEqual(check_account_status.status_code,
                         200)  # assert successful

    def test_raise_value_errors(self):
        """ Test the length of PartyId"""
        self.assertRaises(ValueError,
                          self.momo1.request_to_pay,
                          '36654', '096962', '56797356')
        self.assertRaises(ValueError,
                          self.momo1.request_to_pay,
                          '36654', '0969620978895774', '56797356')
        self.assertRaises(ValueError,
                          self.momo1.request_to_pay,
                          '5', '0969620978', '56797356')

    def test_raise_type_errors(self):
        """Test the type of paramateres"""
        self.assertRaises(TypeError,
                          self.momo1.request_to_pay,
                          12345, '0969620939', '56797356')
        self.assertRaises(TypeError,
                          self.momo1.request_to_pay,
                          '12345', 969620939, '56797356')
        self.assertRaises(TypeError,
                          self.momo1.request_to_pay,
                          '12345', '0969620939', 56797356)


class MTNDisbursementTestCase(TestCase):
    """Test MTN Disbursement methods"""

    def setUp(self):
        self.momo1 = Disbursement()
        self.ref = get_uuid4()
        self.api_user = self.momo1.create_api_user(
            self.momo1.subscription_dis_key)
        self.api_key = self.momo1.create_api_key(
            self.momo1.subscription_dis_key)
        self.api_token = self.momo1.create_api_token(
            self.momo1.subscription_dis_key, 'disbursement')
        self.deposit = self.momo1.deposit('3665', '0969620939', 'therence')

    def test_api_user(self):
        """ Test Sandbox user creation"""
        self.assertEqual(self.api_user.status_code, 201)

    def test_api_key(self):
        """Tesk Api key creaStion"""
        self.assertEqual(self.api_key.status_code, 201)

    def test_api_token(self):
        """ Test API access token creation"""
        self.assertEqual(self.api_token.status_code, 200)

    def test_validate_disbursement_account_holder(self):
        """validate disbursement account"""
        check_account_status = self.momo1.validate_account_holder(
            self.momo1.subscription_dis_key, 'msisdn', '0966776644', 'disbursement')
        self.assertEqual(check_account_status.status_code,
                         200)  # assert successful

    def test_deposit_accepted(self):
        """Test the deposit method"""
        self.assertEqual(self.deposit.status_code,
                         202)  # assert successful accepted

    def test_get_deposit_status_completed(self):
        """Test get transer status method"""
        get_deposit_status = self.momo1.get_transaction_status(
            'deposit', self.momo1.x_reference_id)  # check the payment status
        # assert completed successfullys
        self.assertEqual(get_deposit_status.status_code, 200)

    def test_raise_value_errors(self):
        """ Test the length of PartyId"""
        self.assertRaises(ValueError,
                          self.momo1.deposit,
                          '36654', '096962', '56797356')
        self.assertRaises(ValueError,
                          self.momo1.deposit,
                          '36654', '0969620978895774', '56797356')
        self.assertRaises(ValueError,
                          self.momo1.deposit,
                          '5', '0969620978', '56797356')

    def test_raise_type_errors(self):
        """Test the type of paramateres"""
        self.assertRaises(TypeError,
                          self.momo1.deposit,
                          12345, '0969620939', '56797356')
        self.assertRaises(TypeError,
                          self.momo1.deposit,
                          '12345', 969620939, '56797356')
        self.assertRaises(TypeError,
                          self.momo1.deposit,
                          '12345', '0969620939', 56797356)
