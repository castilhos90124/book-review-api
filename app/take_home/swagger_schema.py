from take_home.serializers import (BookDetailSerializer,
                                                  BookSerializer)
from drf_yasg import openapi
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema

LIST = {
    'name': 'list',
    'decorator': swagger_auto_schema(
        manual_parameters=[Parameter(name='book_title', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY, required=True)],
        responses={200: BookSerializer},
    )
}

RETRIEVE = {
    'name': 'retrieve',
    'decorator': swagger_auto_schema(
        responses={200: BookDetailSerializer},
    )
}
