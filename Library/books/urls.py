from django.urls import path
from .views import library_view

urlpatterns = [
    path("library/", library_view, name="library"),
]
