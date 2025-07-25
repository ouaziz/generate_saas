
from rest_framework import serializers
from apps.{{ app_name }}.models import {{ model_name }}


class {{ model_name }}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{ model_name }}
        fields = '__all__'
