from django.urls import path
from .views import library_view, search_view , save_book_view

urlpatterns = [
    path("library/", library_view, name="library"),
    path("search/", search_view, name="search"),
    path("save/", save_book_view, name="save-book"),
]
