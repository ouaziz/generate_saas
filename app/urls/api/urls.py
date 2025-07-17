
from rest_framework.routers import DefaultRouter
from {{ app_name }}.views.{{ name }}.api.views import *
from django.urls import path, include

router = DefaultRouter()

router.register(r'{{ name }}s', {{ name }}ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
    