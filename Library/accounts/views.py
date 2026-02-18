import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        res = requests.post(
            "http://127.0.0.1:8000/api/auth/login/",
            json={"username": username, "password": password},
        )

        if res.status_code != 200:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})
        
        data = res.json()
        response = redirect("library")
        response.set_cookie(
            "access",
            data["access"],
            httponly=True,
            samesite="Lax",
        )
        return response
    
    return render(request, "accounts/login.html")


def logout_view(request):
    response = redirect("login")
    response.delete_cookie("access")
    return response