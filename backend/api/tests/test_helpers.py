import unittest
from unittest.mock import patch

from api.helpers import get_uuid4, basic_auth

class TestHelperFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("**** Test Helper Functions ****")

    @patch('requests.get')
    def test_get_uuid4_successful_response(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.text = "test-uuid"
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        uuid = get_uuid4()

        self.assertEqual(uuid, "test-uuid")
        mock_get.assert_called_once_with("https://www.uuidgenerator.net/api/version4", headers={}, data={})

    @patch('requests.get')
    def test_get_uuid4_failed_response(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.text = 'none'
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        uuid = get_uuid4()

        self.assertEqual(uuid, "none")
        mock_get.assert_called_once_with("https://www.uuidgenerator.net/api/version4", headers={}, data={})

    def test_basic_auth(self):
        username = "test_username"
        password = "test_password"
        expected_token = "Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk"

        token = basic_auth(username, password)

        self.assertEqual(token, expected_token)

if __name__ == '__main__':
    unittest.main()