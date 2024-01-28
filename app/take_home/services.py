import json
from http.client import HTTPResponse

import requests
from take_home.messages import Message
from take_home.models import Book, BookReview
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import APIException


class BookService:

    def __init__(self):
        self.BOOK_API_URL = 'https://gutendex.com/books/'

    def get_books_by_title(self, book_title: str) -> list:
        query_param = F'?search={book_title}'
        return self.__get_book_data(query_param)['results']

    def get_book_details(self, book_id: str) -> dict:
        book_details = self.__get_book_data(book_id)
        book_details['rating'] = self.__get_book_average_rating(book_id)
        book_details['reviews'] = self.__get_book_reviews(book_id)
        return book_details

    def __get_book_data(self, query_param: str = ''):
        try:
            response = self.get_external_api_response(query_param)
            if response.status_code != status.HTTP_200_OK:
                raise APIException(Message.gutendex_error())
            return json.loads(response.text)
        except requests.exceptions.RequestException:
            raise APIException(Message.gutendex_error())

    def get_external_api_response(self, query_param: str) -> HTTPResponse:
        return requests.get(F'{self.BOOK_API_URL}{query_param}')

    @staticmethod
    def __get_book_average_rating(book_id: str) -> float:
        try:
            book = Book.objects.get(id=book_id)
        except ObjectDoesNotExist:
            return None
        return round(float(book.rating_sum) / book.rating_count, 1)

    @staticmethod
    def __get_book_reviews(book_id: str) -> list:
        book_reviews_queryset = BookReview.objects.filter(book_id=book_id).values_list('review', flat=True)
        return list(book_reviews_queryset)

    @staticmethod
    def update_book_rating(book_id: int, rating: int):
        book, created = Book.objects.get_or_create(
            id=book_id, defaults={'rating_sum': rating, 'rating_count': 1}
        )
        if not created:
            book.rating_sum += rating
            book.rating_count += 1
            book.save()
