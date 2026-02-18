import requests 

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books(query):
    params = {
        'q': query,
        'maxResults': 5,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data


from books.models import Book
import requests

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books(query):
    params = {
        "q": query,
        "maxResults": 5,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


def save_book(item):
    info = item.get("volumeInfo", {})

    book, created = Book.objects.get_or_create(
        google_book_id=item.get("id"),
        defaults={
            "title": info.get("title", "No Title"),
            "total_pages": info.get("pageCount", 0),
        }
    )
    return book


