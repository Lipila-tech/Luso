import unittest
from unittest.mock import patch
from uuid import UUID
from api.helpers import generate_reference_id, basic_auth, is_payment_details_valid


class TestHelperFunctions(unittest.TestCase):
    @patch('requests.get')
    def test_get_uuid4_successful_response(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.text = "test-uuid"
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        uuid = generate_reference_id()

        self.assertEqual(uuid, "test-uuid")
        mock_get.assert_called_once_with(
            "https://www.uuidgenerator.net/api/version4", headers={}, data={})
        
    def test_get_uuid4_returns_valid_uuid(self):
        """
        Tests that generate_reference_id returns a valid UUID string.
        """
        response_text = generate_reference_id()
        try:
            # Attempt to convert the response to a UUID object
            UUID(response_text)
            self.assertTrue(True)  # Test passes if conversion is successful
        except ValueError:
            self.fail("generate_reference_id did not return a valid UUID string.")

    @patch('requests.get')
    def test_get_uuid4_failed_response(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.text = 'none'
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        uuid = generate_reference_id()

        self.assertEqual(uuid, "none")
        mock_get.assert_called_once_with(
            "https://www.uuidgenerator.net/api/version4", headers={}, data={})

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
