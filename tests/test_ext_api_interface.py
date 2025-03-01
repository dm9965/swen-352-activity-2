import unittest
from library import ext_api_interface
from unittest.mock import Mock
import requests
import json

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.api = ext_api_interface.Books_API()
        self.book = "learning python"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())

    def test_make_request_True(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

    def test_make_request_connection_error(self):
        ext_api_interface.requests.get = Mock(side_effect=requests.ConnectionError)
        url = "some url"
        self.assertEqual(self.api.make_request(url), None)

    def test_make_request_False(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(self.api.make_request(""), None)

    def test_get_ebooks(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.get_ebooks(self.book), self.books_data)
    
    def test_get_ebooks_empty(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_ebooks(""), [])

    def test_is_book_available_true(self):
        self.api.make_request = Mock(return_value={'docs': [{'title': 'Testing Book'}]})
        self.assertTrue(self.api.is_book_available("Testing Book"))

    def test_is_book_available_false(self):
        self.api.make_request = Mock(return_value={'docs': []})
        self.assertFalse(self.api.is_book_available("Testing Book"))

    def test_books_by_author(self):
        self.api.make_request = Mock(return_value={'docs': [{'title_suggest': 'Testers Biography'}, {'title_suggest': 'Another Book'}]})
        self.assertEqual(self.api.books_by_author("Jarred Reepmeyer"), ['Testers Biography', 'Another Book'])

    def test_books_by_author_empty(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.books_by_author(""), [])

    def test_get_book_info_full(self):
        self.api.make_request = Mock(return_value={'docs': [{'title': 'Testers Biography', 'publisher': 'Reepmeyer Publishing', 'publish_year': '2025', 'language': 'English'}]})
        self.assertEqual(self.api.get_book_info("Testers Biography"), [{'title': 'Testers Biography', 'publisher': 'Reepmeyer Publishing', 'publish_year': '2025', 'language': 'English'}])

    def test_get_book_info_empty(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_book_info(""), [])



