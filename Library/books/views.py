import requests
from django.shortcuts import render, redirect

import json

def library_view(request):
    access = request.COOKIES.get("access")

    if not access:
        return redirect("login")

    res = requests.get(
        "http://127.0.0.1:8000/api/books/library/",
        cookies={"access": access}, 
    )

    data = res.json() if res.status_code == 200 else {}

    return render(
        request,
        "books/library.html",
        {
            "reading": data.get("reading", []),
            "finished": data.get("finished", []),
        },
    )

def search_view(request):
    access = request.COOKIES.get("access")

    if not access:
        return redirect("login")

    query = request.GET.get("q")
    results = []

    if query:
        res = requests.get(
            "http://127.0.0.1:8000/api/books/search/",
            params={"q": query},
            cookies={"access": access},
        )

        if res.status_code == 200:
            data = res.json()
            results = data.get("items", [])

    return render(
        request,
        "books/search.html",
        {
            "results": results,
            "query": query,
        },
    )


def save_book_view(request):
    if request.method != "POST":
        return redirect("search")

    access = request.COOKIES.get("access")
    if not access:
        return redirect("login")

    google_book_id = request.POST.get("google_book_id")
    if not google_book_id:
        return redirect("search")

    # Fetch book again via API (clean & safe)
    res = requests.get(
        "https://www.googleapis.com/books/v1/volumes/" + google_book_id
    )

    if res.status_code != 200:
        return redirect("search")

    item = res.json()

    requests.post(
        "http://127.0.0.1:8000/api/books/save/",
        json={"item": item},
        cookies={"access": access},
    )

    return redirect("library")
