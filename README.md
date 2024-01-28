# Take Home - Book Review Application

## Getting Started
Dependencies:
* Docker - See [Get Docker](https://docs.docker.com/get-docker/)
* Docker Compose - Installed with Docker Desktop, See [Install Docker Compose](https://docs.docker.com/compose/install/)
* Make - See [Install Make](https://linuxhint.com/install-make-ubuntu/)

To start the application, open a terminal on the root folder and run:

```
make run
```
It can be accessed in http://localhost:8010/

To end the service, press `Ctrl+C`

## Testing

To run integration and unit tests, run:
```
make test
```

## Problem Statement
Many people like to read books, but it is difficult to know if a book is good or not before reading it. 
So I decided to create a book rating API, which will allow us to search for books, rate and review the books we have read.

In order to do that, the API will get books data from a third party called [Gutendex API](https://gutendex.com/)

## Features

### Search for books
It is possible to search for books, providing the title of the book and getting the information from Gutendex API.

Example of request:
```
curl --location 'http://127.0.0.1:8010/books?book_title=Frankenstein'
```

Example of response:
```
{
    "books": [
        {
            "id": 84,
            "title": "Frankenstein; Or, The Modern Prometheus",
            "authors": [
                {
                    "name": "Shelley, Mary Wollstonecraft",
                    "birth_year": 1797,
                    "death_year": 1851
                }
            ],
            "languages": [
                "en"
            ],
            "download_count": 60961
        },
        {
            "id": 62405,
            "title": "Frankenstein, ou le Prométhée moderne Volume 2 (of 3)",
            "authors": [
                {
                    "name": "Shelley, Mary Wollstonecraft",
                    "birth_year": 1797,
                    "death_year": 1851
                }
            ],
            "languages": [
                "fr"
            ],
            "download_count": 74
        }
    ]
}
```
### Review a book
To add a book review, we need to provide the book id (same as the Gutendex API), the rating (integer from 1 to 5) and the review comment.


Example of request:
```
curl --location 'http://127.0.0.1:8010/books/' \
--header 'Content-Type: application/json' \
--data '{
    "book_id": 84,
    "rating": 5,
    "review": "An amazing book!"
}'
```

### Get details of a specific book
It is possible to get more details of a specific book, then we can see the average rating and the reviews of the desired book. 

To provide this reponse, our API will get data from Gutendex API, and also from our own database.

Example of request:
```
curl --location 'http://127.0.0.1:8010/books/84'
```
Example of response:
```
{
    "id": 84,
    "title": "Frankenstein; Or, The Modern Prometheus",
    "authors": [
        {
            "name": "Shelley, Mary Wollstonecraft",
            "birth_year": 1797,
            "death_year": 1851
        }
    ],
    "languages": [
        "en"
    ],
    "download_count": 60961,
    "rating": 3.5,
    "reviews": [
        "Awesome book",
        "Not good"
    ]
}
```

## Documentation
You can access the swagger documentation [here](http://127.0.0.1:8010/docs):
```
http://127.0.0.1:8010/docs
```