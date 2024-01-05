# pages/views.py

from django.shortcuts import render

def home(request):
    return render(request, "pages/homepage.html", {})