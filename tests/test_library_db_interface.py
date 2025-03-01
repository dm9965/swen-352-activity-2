import unittest
from unittest.mock import Mock, call

from library import library_db_interface


class TestLibbraryDBInterface(unittest.TestCase):

    def setUp(self):
        self.db_interface = library_db_interface.Library_DB()

    def test_insert_patron_in_db(self):
        data = {'fname': 'name', 'lname': 'name', 'age': '50', 'memberID': '1234',
                'borrowed_books': []}
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=data)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), None)

    def test_insert_not_patron(self):
        data = None
        self.assertEqual(self.db_interface.insert_patron(data), None)

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(side_effect=lambda x: 10 if x == data else 0)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)

    def test_get_patron_count(self):
        data = [1, 2, 3, 4, 5, 6]
        self.db_interface.db.all = Mock(return_value=data)
        self.assertEqual(self.db_interface.get_patron_count(), len(data))

    def test_get_patrons(self):
        data = [1, 2, 3, 4, 5, 6]
        self.db_interface.db.all = Mock(return_value=data)
        self.assertEqual(self.db_interface.get_all_patrons(), data)

    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()

    def test_update_not_patron(self):
        data = None
        self.assertEqual(self.db_interface.update_patron(data), None)

    def test_retrieve_patron(self):
        data = [{'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': '1234',
                 'borrowed_books': []}, ]
        self.db_interface.db.search = Mock(return_value=data)
        self.assertEqual(self.db_interface.convert_patron_to_db_format(self.db_interface.retrieve_patron('1234')),
                         data[0])

    def test_retrieve_patron_no_results(self):
        data = []
        self.db_interface.db.search = Mock(return_value=data)
        self.assertIsNone(self.db_interface.retrieve_patron('1234'))

    def test_close_db(self):
        db_close_mock = Mock()
        self.db_interface.db.close = db_close_mock
        self.db_interface.close_db()
        db_close_mock.assert_called()


    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()

        patron_mock.get_fname = Mock(return_value=1)
        patron_mock.get_lname = Mock(return_value=2)
        patron_mock.get_age = Mock(return_value=3)
        patron_mock.get_memberID = Mock(return_value=4)
        patron_mock.get_borrowed_books = Mock(return_value=5)
        self.assertEqual(self.db_interface.convert_patron_to_db_format(patron_mock),
                         {'fname': 1, 'lname': 2, 'age': 3, 'memberID': 4,
                          'borrowed_books': 5})
