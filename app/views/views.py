
from rest_framework import viewsets
from {{ app_name }}.models import *
from {{ app_name }}.views.{{ model_name }}.api.serializers import *


class {{ model_name }}ViewSet(viewsets.ModelViewSet):
    queryset = {{ model_name }}.objects.all()
    serializer_class = {{ model_name }}Serializer

    