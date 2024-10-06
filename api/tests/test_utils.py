import unittest
from unittest.mock import patch
from uuid import UUID
from api.utils import basic_auth, is_payment_details_valid, generate_transaction_id
import uuid


class TestTransactionId(unittest.TestCase):

    def test_returns_string(self):
        """Test if the function returns a string."""
        result = generate_transaction_id()
        self.assertIsInstance(result, str)

    def test_is_valid_uuid4(self):
        """Test if the returned string is a valid UUID4."""
        result = generate_transaction_id()
        try:
            uuid_obj = uuid.UUID(result, version=4)
            # Check if the UUID is valid and is a version 4 UUID
            self.assertEqual(uuid_obj.version, 4)
        except ValueError:
            self.fail("generate_transaction_id returned an invalid UUID")

    def test_unique_ids(self):
        """Test if each call returns a unique ID."""
        result1 = generate_transaction_id()
        result2 = generate_transaction_id()
        self.assertNotEqual(result1, result2)


class TestUtilFunctions(unittest.TestCase):
    def test_basic_auth(self):
        username = "test_username"
        password = "test_password"
        expected_token = "Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk"

        token = basic_auth(username, password)

        self.assertEqual(token, expected_token)

    def test_is_payment_details_valid_positional_valid(self):
        """
        Tests that the function returns True for valid positional arguments.
        """
        valid_args = ('20', '0987654321', 'DEF456')
        self.assertTrue(is_payment_details_valid(*valid_args))

    def test_is_payment_details_valid_missing_argument(self):
        """
        Tests that the function raises a ValueError for missing arguments.
        """
        with self.assertRaises(ValueError) as cm:
            is_payment_details_valid(amount='10', payer='1234567890')
        self.assertEqual(str(
            cm.exception), "Missing or invalid arguments. Expected 'amount', 'payer', and 'reference'.")


if __name__ == '__main__':
    unittest.main()
