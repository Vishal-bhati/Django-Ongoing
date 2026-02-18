from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from books.services.google_books import search_books, save_book
from books.models import UserBook
from books.services.library import currently_reading, recently_finished


User = get_user_model()

class BookSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get("q")

        if not query:
            return Response(
                {"error": "Query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = search_books(query)
        return Response(data)
    


class BookSaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item = request.data.get("item")

        if not item:
            return Response(
                {"error": "Book data is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book = save_book(item)

        user = User.objects.first()  # For demo purposes, we use the first user

        UserBook.objects.get_or_create(
            user=user,
            book=book,
            )
        
        return Response(
            {"message": "Book saved", "title":book.title},
            status=status.HTTP_201_CREATED
        )
    
class MyLibraryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        reading = currently_reading(user)
        finsished = recently_finished(user) 

        return Response({
            "username": user.username,
            "reading": [
                {
                    "id": ub.id,
                    "title": ub.book.title,
                    "current_page": ub.current_page,
                }
                for ub in reading
            ],
            "finished": [
                {
                    "id": ub.id,
                    "title": ub.book.title,
                    "finished_at": ub.last_updated,
                }
                for ub in finsished
            ]
        })
    
class UpdateProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get("book_id")
        current_page = request.data.get("current_page")

        if book_id is None or current_page is None:
            return Response(
                {"error": "Book ID and current page are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user

        user_book = get_object_or_404(
            UserBook,  
            user=user,
            book_id=book_id
        )

        user_book.update_progress(int(current_page))

        return Response({
            "message": "Progress updated",
            "book_title": user_book.book.title,
            "current_page": user_book.current_page,
            "status": user_book.status,
            "last_updated": user_book.last_updated,
        })