import json
from unittest.mock import patch

from take_home.services import BookService
from take_home.tests.gutendex_mock import (
    GET_BOOK_BY_TITLE_MOCK, GET_ERROR)
from take_home.models import Book, BookReview
from django.test import TestCase
from rest_framework.exceptions import APIException


class BookUnitTest(TestCase):

    def setUp(self):
        self.service = BookService()

    def test_update_book_rating_created(self):
        book_id = 1
        rating = 5

        BookService.update_book_rating(book_id, rating)

        book = Book.objects.get(id=book_id)

        self.assertEqual(book.rating_sum, rating)
        self.assertEqual(book.rating_count, 1)

    def test_update_book_rating_not_created(self):
        book_id = 1
        rating_sum = 9
        rating_count = 2
        rating = 4

        Book(id=book_id, rating_sum=rating_sum, rating_count=rating_count).save()
        BookService.update_book_rating(book_id, rating)

        book = Book.objects.get(id=book_id)

        self.assertEqual(book.rating_sum, rating_sum + rating)
        self.assertEqual(book.rating_count, rating_count + 1)

    def test_get_book_reviews(self):
        book_id = 1
        expected_reviews = ['Very interesting!', 'Awesome']

        Book(id=book_id, rating_sum=9, rating_count=2).save()
        BookReview(book_id=book_id, rating=4, review=expected_reviews[0]).save()
        BookReview(book_id=book_id, rating=5, review=expected_reviews[1]).save()
        reviews = BookService._BookService__get_book_reviews(book_id)

        self.assertEqual(reviews, expected_reviews)

    def test_get_book_average_rating_empty(self):
        average_rating = BookService._BookService__get_book_average_rating(book_id=1)

        self.assertEqual(average_rating, None)

    def test_get_book_average_rating(self):
        book_id = 1
        Book(id=book_id, rating_sum=7, rating_count=3).save()

        average_rating = BookService._BookService__get_book_average_rating(book_id)

        self.assertEqual(average_rating, 2.3)

    @patch.object(BookService, 'get_external_api_response')
    def test_get_book_data(self, external_api_mock):
        external_api_mock.return_value = GET_BOOK_BY_TITLE_MOCK
        book_data = self.service._BookService__get_book_data()
        self.assertEqual(book_data, json.loads(GET_BOOK_BY_TITLE_MOCK.text))

    @patch.object(BookService, 'get_external_api_response')
    def test_get_book_data_api_exception(self, external_api_mock):
        external_api_mock.return_value = GET_ERROR
        with self.assertRaises(APIException):
            self.service._BookService__get_book_data()
