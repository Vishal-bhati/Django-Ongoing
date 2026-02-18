from django.urls import path
from .views import BookSearchAPIView , BookSaveAPIView , MyLibraryAPIView , UpdateProgressAPIView

urlpatterns = [
    path("search/", BookSearchAPIView.as_view(), name="book-search"),
    path("save/", BookSaveAPIView.as_view(), name="book-save"),
    path("library/", MyLibraryAPIView.as_view(), name="my-library"),
    path("progress/", UpdateProgressAPIView.as_view(), name="my-progress"),
]
