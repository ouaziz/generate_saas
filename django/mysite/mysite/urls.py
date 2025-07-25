"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.urls import include

urlpatterns = [
    path('', include('pages.urls')),
    path('connexion/', include('connexion.urls')),
    path('admin/', admin.site.urls),
    path('invoicing/', include('apps.invoicing.urls.client.html.urls')),
    path('invoicing/', include('apps.invoicing.urls.invoice.html.urls')),
    path('crm/', include('apps.crm.urls.contact.html.urls')),
    path('crm/', include('apps.crm.urls.lead.html.urls')),
    path('crm/', include('apps.crm.urls.task.html.urls')),
]


def custom_404_handler(request, exception):
    return redirect('error_404_1_url')
def custom_500_handler(request):
    return redirect('error_500_url')
handler404 = custom_404_handler
handler500 = custom_500_handler
