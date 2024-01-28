import json


class MockResponse:

    def __init__(self, status_code: int, text: str = ''):
        self.status_code = status_code
        self.text = text


book_detail = {
    'id': 84,
    'title': 'Frankenstein; Or, The Modern Prometheus',
    'authors': [{'name': 'Shelley, Mary Wollstonecraft', 'birth_year': 1797, 'death_year': 1851}],
    'translators': [],
    'subjects': ['Frankensteins monster (Fictitious character) -- Fiction'],
    'bookshelves': ['Gothic Fiction'],
    'languages': ['en'],
    'copyright': False,
    'media_type': 'Text',
    'formats': {
        'application/epub+zip': 'https://www.gutenberg.org/ebooks/84.epub.images',
    },
    'download_count': 16301
}

book_by_title = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [
        book_detail
    ]
}


GET_BOOK_BY_TITLE_MOCK = MockResponse(status_code=200, text=json.dumps(book_by_title))
GET_BOOK_DETAIL_MOCK = MockResponse(status_code=200, text=json.dumps(book_detail))
GET_ERROR = MockResponse(status_code=500)
