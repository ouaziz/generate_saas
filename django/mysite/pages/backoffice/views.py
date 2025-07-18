# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="login_page_url")
def dashboard_page(request):
    return render(request, 'pages/backoffice/index.html')