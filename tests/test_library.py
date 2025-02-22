import unittest
from unittest.mock import Mock, MagicMock
from library import library, patron
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        self.patron = patron.Patron("Firstname", "Lastname", 18, 12345)
        self.books_data = [{'title': 'Learning Python', 'author': 'Mark Lutz', 'ebook_count': 3}, {'title': 'Learning Python (Learning)', 'author': 'Rapid Python', 'ebook_count': 1}, {'title': 'Learning Python', 'author': 'Rapid Python', 'ebook_count': 1}, {'title': 'Learn to Program Using Python', 'author': 'We Love Python', 'ebook_count': 1}, {'title': 'Aprendendo Python', 'author': 'Rapidemente Python', 'ebook_count': 0}, {'title': 'Python Basics', 'author': 'Basic Python Author', 'ebook_count': 1}]

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('not an ebook'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 7)

    def test_is_book_by_author(self):
        self.lib.api.books_by_author = Mock(return_value=["Learning python"])
        self.assertTrue(self.lib.is_book_by_author("Mark Lutz", "Learning Python"))

    def test_is_book_not_by_author(self):
        self.lib.api.books_by_author = Mock(return_value=["Learning python"])
        self.assertFalse(self.lib.is_book_by_author("Mark Lutz", "different python book"))

    def test_get_languages_for_book(self):
        languages = {'eng', 'ger', 'hin', 'por'}
        self.lib.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_languages_for_book('Learning Python'), languages)

    def test_get_wrong_languages_for_book(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        languages = {'eng', 'ger'}
        self.assertNotEqual(self.lib.get_languages_for_book('Learning Python'), languages)

    def test_register_patron(self):
        self.lib.register_patron = Mock(return_value=(self.patron.get_fname(), self.patron.get_lname(), self.patron.get_age(), self.patron.get_memberID()))
        self.assertEqual(self.lib.is_patron_registered(self.patron), True)

    def test_patron_not_registered(self):
        unregister_patron = patron.Patron("Badname", "Lastname", 33, 2134)
        self.assertFalse(self.lib.is_patron_registered(unregister_patron))

    def test_borrow_book(self):
        book = "Learning Python"
        self.lib.borrow_book(book, self.patron)
        self.assertGreater(len(self.patron.borrowed_books), 0)

    def test_is_book_borrowed(self):
        book = "learning python"
        self.lib.borrow_book(book, self.patron)
        self.assertTrue(self.lib.is_book_borrowed(book, self.patron))

    def test_book_not_borrowed(self):
        not_borrowed_book = "another python book"
        borrowed_book = "Learning Python"
        self.lib.borrow_book(borrowed_book, self.patron)
        self.assertFalse(self.lib.is_book_borrowed(not_borrowed_book, self.patron))

    def test_return_borrowed_book(self):
        book = "Learning Python"
        self.lib.borrow_book(book, self.patron)
        self.lib.return_borrowed_book(book, self.patron)
        self.assertEqual(len(self.patron.borrowed_books), 0)

    def test_return_not_borrowed_book(self):
        not_borrowed_book = "another python book"
        book = "Learning Python"
        self.lib.borrow_book(book, self.patron)
        self.lib.return_borrowed_book(not_borrowed_book, self.patron)
        self.assertGreater(len(self.patron.borrowed_books), 0)

