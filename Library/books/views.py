from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

def library_view(request):
    return render(request, "books/library.html")
