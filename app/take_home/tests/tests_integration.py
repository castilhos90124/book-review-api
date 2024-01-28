from unittest.mock import patch

from take_home.services import BookService
from take_home.tests.gutendex_mock import (
    GET_BOOK_BY_TITLE_MOCK, GET_BOOK_DETAIL_MOCK, GET_ERROR)
from take_home.messages import Message
from take_home.models import Book, BookReview
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class BookAPITest(APITestCase):
    def setUp(self):
        super().setUp()
        self.BASE_URL = reverse('books-list')
        self.BOOK_ATTRIBUTES = {'id', 'title', 'authors', 'languages', 'download_count'}
        self.REVIEW_ATTRIBUTES = {'id', 'book_id', 'rating', 'review'}
        self.BOOK_DETAIL_ATTRIBUTES = {'id', 'title', 'authors', 'languages', 'download_count', 'rating', 'reviews'}
        self.DEFAULT_BODY_PARAMS = {'book_id': 1, 'rating': 4, 'review': 'An interesting book.'}

    @patch.object(BookService, 'get_external_api_response')
    def test_get_books(self, external_api_mock):
        external_api_mock.return_value = GET_BOOK_BY_TITLE_MOCK

        query_param = 'book_title=Frankenstein'
        url = f'{self.BASE_URL}?{query_param}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.BOOK_ATTRIBUTES, set(response.data['books'][0]))

    def test_get_books_without_query_param(self):
        response = self.client.get(self.BASE_URL)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], Message.book_title_not_informed())

    @patch.object(BookService, 'get_external_api_response')
    def test_external_api_error(self, external_api_mock):
        external_api_mock.return_value = GET_ERROR

        query_param = 'book_title=Frankenstein'
        url = f'{self.BASE_URL}?{query_param}'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['detail'], Message.gutendex_error())

    def test_post_book_review(self):
        response = self.client.post(self.BASE_URL, self.DEFAULT_BODY_PARAMS)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.REVIEW_ATTRIBUTES, set(response.data))

        self.client.post(self.BASE_URL, self.DEFAULT_BODY_PARAMS)
        book = Book.objects.get(id=self.DEFAULT_BODY_PARAMS['book_id'])

        self.assertEqual(book.id, self.DEFAULT_BODY_PARAMS['book_id'])
        self.assertEqual(book.rating_sum, self.DEFAULT_BODY_PARAMS['rating'] * 2)
        self.assertEqual(book.rating_count, 2)

    def test_post_book_review_with_wrong_rating(self):
        self.DEFAULT_BODY_PARAMS.update({'rating': 6})
        response = self.client.post(self.BASE_URL, self.DEFAULT_BODY_PARAMS)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_book_review_without_review(self):
        del self.DEFAULT_BODY_PARAMS['review']

        response = self.client.post(self.BASE_URL, self.DEFAULT_BODY_PARAMS)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(BookService, 'get_external_api_response')
    def test_get_book_details(self, external_api_mock):
        external_api_mock.return_value = GET_BOOK_DETAIL_MOCK

        book_id = 1
        rating_sum = 9
        rating_count = 2
        reviews = ['Very interesting!', 'Awesome']

        Book(id=book_id, rating_sum=rating_sum, rating_count=rating_count).save()
        BookReview(book_id=book_id, rating=4, review=reviews[0]).save()
        BookReview(book_id=book_id, rating=5, review=reviews[1]).save()

        response = self.client.get(F'{self.BASE_URL}{book_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.BOOK_DETAIL_ATTRIBUTES, set(response.data))
        self.assertEqual(response.data['rating'], round(float(rating_sum) / rating_count, 1))
        self.assertEqual(len(response.data['reviews']), rating_count)
        self.assertEqual(response.data['reviews'][0], reviews[0])
        self.assertEqual(response.data['reviews'][1], reviews[1])

    @patch.object(BookService, 'get_external_api_response')
    def test_get_book_details_without_reviews(self, external_api_mock):
        external_api_mock.return_value = GET_BOOK_DETAIL_MOCK

        book_id = 1

        response = self.client.get(F'{self.BASE_URL}{book_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.BOOK_DETAIL_ATTRIBUTES, set(response.data))
        self.assertEqual(response.data['rating'], None)
        self.assertEqual(response.data['reviews'], [])
