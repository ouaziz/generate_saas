import json
import os
from jinja2 import Template
import shutil

with open("schema.json") as f:
    schema = json.load(f)

PROJECT_NAME = schema["project"]
MODELS = schema["models"]
TEMPLATES = schema["templates"]

os.makedirs("generated", exist_ok=True)


# ==== templates ===
#  reade templatefrom templates/ and create 4 files for each template with schema.json
for template in TEMPLATES:
    os.makedirs(f"generated/templates/{template['name']}", exist_ok=True)
    name = template["name"]
    files = template["files"]
    shutil.copy(f"templates/{files['list']}", f"generated/templates/{name}/{files['list']}")
    shutil.copy(f"templates/{files['detail']}", f"generated/templates/{name}/{files['detail']}")
    shutil.copy(f"templates/{files['confirm_delete']}", f"generated/templates/{name}/{files['confirm_delete']}")
    shutil.copy(f"templates/{files['form']}", f"generated/templates/{name}/{files['form']}")

# === models.py ===
model_template = Template("""
from django.db import models

{% for model in models %}
class {{ model.name }}(models.Model):
    {% for name, field in model.fields.items() %}
    {{ name }} = models.{{ field }}
    {% endfor %}
{% endfor %}
""")

with open("generated/models.py", "w") as f:
    f.write(model_template.render(models=MODELS))

# === serializers.py ===
serializer_template = Template("""
from rest_framework import serializers
from .models import *

{% for model in models %}
class {{ model.name }}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{ model.name }}
        fields = '__all__'
{% endfor %}
""")

with open("generated/serializers.py", "w") as f:
    f.write(serializer_template.render(models=MODELS))

# === views.py ===
views_template = Template("""
from rest_framework import viewsets
from .models import *
from .serializers import *

{% for model in models %}
class {{ model.name }}ViewSet(viewsets.ModelViewSet):
    queryset = {{ model.name }}.objects.all()
    serializer_class = {{ model.name }}Serializer
{% endfor %}
""")

with open("generated/views.py", "w") as f:
    f.write(views_template.render(models=MODELS))

# === urls.py ===
urls_template = Template("""
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()
{% for model in models %}
router.register(r'{{ model.name|lower }}s', {{ model.name }}ViewSet)
{% endfor %}

urlpatterns = [
    path('', include(router.urls)),
]
""")

with open("generated/urls.py", "w") as f:
    f.write(urls_template.render(models=MODELS))

print("✅ Code généré dans le dossier /generated")
