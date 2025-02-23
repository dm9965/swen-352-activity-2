import unittest
from library import patron
from unittest.mock import Mock

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.pat = patron.Patron('fname', 'lname', '20', '1234')

    def test_valid_name(self):
        pat = patron.Patron('fname', 'lname', '20', '1234')
        self.assertTrue(isinstance(pat, patron.Patron))

    def test_invalid_name(self):
        self.assertRaises(patron.InvalidNameException, patron.Patron, '1fname', '1lname', '20', '1234')

    def test_add_borrow_book(self):
        book = "Learning Python"
        self.pat.add_borrowed_book(book)
        self.assertIn(book.lower(), self.pat.get_borrowed_books())

    def test_booked_not_added(self):
        good_book = "Learning Go"
        bad_book = "Learning Python"
        self.pat.add_borrowed_book(good_book)
        self.assertNotIn(bad_book.lower(), self.pat.get_borrowed_books())

    def test_get_borrowed_books(self):
        books = ["Learning Python", "Learning Go", "Learning Rust"]
        for book in books:
            self.pat.add_borrowed_book(book)

        self.assertEqual(["learning python", "learning go", "learning rust"], self.pat.get_borrowed_books())

    def test_get_borrowed_books_fail(self):
        books = ["Learning Python", "Learning Go", "Learning Rust"]
        for book in books:
            self.pat.add_borrowed_book(book)

        self.assertNotEqual(["learning java", "learning lua", "learning javascript"], self.pat.get_borrowed_books())

    def test_return_borrowed_book(self):
        books = ["Learning Python", "Learning Go", "Learning Rust"]
        for book in books:
            self.pat.add_borrowed_book(book)
        self.pat.return_borrowed_book(books[0])
        self.assertEqual(["learning go", "learning rust"], self.pat.get_borrowed_books())

    def test_return_borrowed_book_does_not_exist(self):
        books = ["Learning Python", "Learning Go", "Learning Rust"]
        for book in books:
                self.pat.add_borrowed_book(book)
        self.pat.return_borrowed_book('Learning Javascript')
        self.assertEqual(["learning python", "learning go", "learning rust"], self.pat.get_borrowed_books())

    def test_return_borrowed_book_fail(self):
        books = ["Learning Python", "Learning Go", "Learning Rust"]
        for book in books:
                self.pat.add_borrowed_book(book)
        self.pat.return_borrowed_book('Learning Go')
        self.assertNotEqual(["learning go", "learning rust"], self.pat.get_borrowed_books())

    def test_get_fname(self):
        self.assertEqual(self.pat.get_fname(), "fname")

    def test_get_fname_fail(self):
        self.assertNotEqual(self.pat.get_fname(), "lastName")

    def test_get_lname(self):
        self.assertEqual(self.pat.get_lname(), "lname")

    def test_get_lname_fail(self):
        self.assertNotEqual(self.pat.get_lname(), "lastName")

    def test_get_age(self):
        self.assertEqual(self.pat.get_age(), "20")

    def test_get_age_fail(self):
        self.assertNotEqual(self.pat.get_age(), "25")

    def test_get_memberID(self):
        self.assertEqual(self.pat.get_memberID(), "1234")

    def test_get_memberID_fail(self):
        self.assertNotEqual(self.pat.get_fname(), "3412")