# Create your views here.
from django.shortcuts import render

def index_page(request):
    return render(request, 'pages/landingpage/index.html')

def error_404_1(request):
    return render(request, 'pages/landingpage/errors/error-404-1.html')

def error_500(request):
    return render(request, 'pages/landingpage/errors/error-500.html')

