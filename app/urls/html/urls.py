from django.urls import path
from apps.{{ app_name }}.views.{{ name }}.html.views import (
    List, Detail,
    Create, Update, Delete,
)

urlpatterns = [
    path("{{ name }}s/",                    List.as_view(),   name="{{ name }}-list"),
    path("{{ name }}s/new/",                Create.as_view(), name="{{ name }}-create"),
    path("{{ name }}s/<uuid:pk>/",          Detail.as_view(), name="{{ name }}-detail"),
    path("{{ name }}s/<uuid:pk>/edit/",     Update.as_view(), name="{{ name }}-update"),
    path("{{ name }}s/<uuid:pk>/delete/",   Delete.as_view(), name="{{ name }}-delete"),
]