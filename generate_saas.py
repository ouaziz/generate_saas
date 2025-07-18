import json
import os
from jinja2 import Template
import shutil


# remove folder
if os.path.exists("generated"):
    shutil.rmtree("generated")
print(f"✅ cleaning folder")
 

with open("schema.json") as f:
    schema = json.load(f)
print(f"✅ reading schema.json")

PROJECT_NAME = schema["project"]
MODELS = schema["models"]
TEMPLATES = schema["templates"]
FORMS = schema["forms"]

app_name = schema["app_name"]
os.makedirs(f"generated/{ app_name }", exist_ok=True)


# ==== templates ===#======================================================================================================#
#  reade templatefrom templates/ and create 4 files for each template with schema.json
for template in TEMPLATES:
    name = template["name"]
    os.makedirs(f"generated/{ app_name }/templates/{template['name']}", exist_ok=True)

    shutil.copy(f"app/templates/list.html", f"generated/{ app_name }/templates/{name}/list.html")
    shutil.copy(f"app/templates/detail.html", f"generated/{ app_name }/templates/{name}/detail.html")
    shutil.copy(f"app/templates/confirm_delete.html", f"generated/{ app_name }/templates/{name}/confirm_delete.html")
    shutil.copy(f"app/templates/form.html", f"generated/{ app_name }/templates/{name}/form.html")

# Lire les templates de base (ils ont {{ name }})
with open("app/templates/list.html", "r") as f:
    # template_list = Template(f.read())
    template_list = f.read()

with open("app/templates/detail.html", "r") as f:
    # template_detail = Template(f.read())
    template_detail = f.read()

with open("app/templates/confirm_delete.html", "r") as f:
    # template_confirm_delete = Template(f.read())
    template_confirm_delete = f.read()

with open("app/templates/form.html", "r") as f:
    # template_form = Template(f.read())
    template_form = f.read()

# Génération des templates avec substitution dynamique de {{ name }}
for template in TEMPLATES:
    name = template["name"]

    static = "{% load static %}"
    i18n = "{% load i18n %}"
    # os.makedirs(f"generated/{ app_name }/templates/{name}", exist_ok=True)

    with open(f"generated/{ app_name.lower() }/templates/{name.lower()}/list.html", "w") as f:
        f.write(template_list.replace("{{ name }}", name).replace("{{ loads }}", static + i18n))

    with open(f"generated/{ app_name.lower() }/templates/{name.lower()}/detail.html", "w") as f:
        f.write(template_detail.replace("{{ name }}", name).replace("{{ loads }}", static + i18n))

    with open(f"generated/{ app_name.lower() }/templates/{name.lower()}/confirm_delete.html", "w") as f:
        f.write(template_confirm_delete.replace("{{ name }}", name).replace("{{ loads }}", static + i18n))

    with open(f"generated/{ app_name.lower() }/templates/{name.lower()}/form.html", "w") as f:
        f.write(template_form.replace("{{ name }}", name).replace("{{ loads }}", static + i18n))
print(f"✅ templates")

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

with open(f"generated/{ app_name.lower() }/models.py", "w") as f:
    f.write(model_template.render(models=MODELS))
print(f"✅ models")

# === serializers.py ===
for model in MODELS:
    name = model["name"]
    os.makedirs(f"generated/{ app_name.lower() }/views/{name.lower()}/api", exist_ok=True)
    shutil.copy(f"app/views/serializers.py", f"generated/{ app_name.lower() }/views/{name.lower()}/api/serializers.py")
    with open("app/views/serializers.py", "r") as f:
        serializer_template = Template(f.read())
    with open(f"generated/{ app_name.lower() }/views/{name.lower()}/api/serializers.py", "w") as f:
        f.write(serializer_template.render(model_name=name, app_name=app_name.lower()))
print(f"✅ serializers")

# === api views.py ===
for model in MODELS:
    name = model["name"]
    os.makedirs(f"generated/{ app_name.lower() }/views/{name.lower()}/api", exist_ok=True)
    shutil.copy(f"app/views/views.py", f"generated/{ app_name.lower() }/views/{name.lower()}/api/views.py")
    with open("app/views/views.py", "r") as f:
        views_template = Template(f.read())
    with open(f"generated/{ app_name.lower() }/views/{name.lower()}/api/views.py", "w") as f:
        f.write(views_template.render(model_name=name, app_name=app_name.lower()))
print(f"✅ views api")

# === html views.py ===
for model in MODELS:
    name = model["name"]
    os.makedirs(f"generated/{ app_name.lower() }/views/{name.lower()}/html", exist_ok=True)
    shutil.copy(f"app/views/views_html.py", f"generated/{ app_name.lower() }/views/{name.lower()}/html/views.py")
    with open("app/views/views_html.py", "r") as f:
        views_template = Template(f.read())
    with open(f"generated/{ app_name.lower() }/views/{name.lower()}/html/views.py", "w") as f:
        f.write(views_template.render(model_name=name, app_name=app_name.lower(), name=name.lower()))
print(f"✅ views")

# === service.py ===
for model in MODELS:
    name = model["name"]
    os.makedirs(f"generated/{ app_name.lower() }/services/{name.lower()}", exist_ok=True)
    shutil.copy(f"app/services.py", f"generated/{ app_name.lower() }/services/{name.lower()}/services.py")
    with open("app/services.py", "r") as f:
        service_template = Template(f.read())
    with open(f"generated/{ app_name.lower() }/services/{name.lower()}/services.py", "w") as f:
        f.write(service_template.render(model_name=name, app_name=app_name.lower(), name=name.lower()))
print(f"✅ services")


# === api - urls.py ===
for model in MODELS:
    name = model["name"]
    os.makedirs(f"generated/{ app_name.lower() }/urls/{name.lower()}/api", exist_ok=True)
    shutil.copy(f"app/urls/api/urls.py", f"generated/{ app_name.lower() }/urls/{name.lower()}/api/urls.py")
    with open("app/urls/api/urls.py", "r") as f:
        urls_template = Template(f.read())
    with open(f"generated/{ app_name.lower() }/urls/{name.lower()}/api/urls.py", "w") as f:
        f.write(urls_template.render(name=name.lower(), app_name=app_name.lower()))
print(f"✅ urls api")

# === html - urls.py ===
for model in MODELS:
    name = model["name"]
    os.makedirs(f"generated/{ app_name.lower() }/urls/{name.lower()}/html", exist_ok=True)
    shutil.copy(f"app/urls/html/urls.py", f"generated/{ app_name.lower() }/urls/{name.lower()}/html/urls.py")
    with open("app/urls/html/urls.py", "r") as f:
        urls_template = Template(f.read())
    with open(f"generated/{ app_name.lower() }/urls/{name.lower()}/html/urls.py", "w") as f:
        f.write(urls_template.render(name=name.lower(), app_name=app_name.lower()))
print(f"✅ urls")

# === apps.py ===
with open("app/apps.py", "r") as f:
    apps_template = Template(f.read())
with open(f"generated/{ app_name.lower() }/apps.py", "w") as f:
    f.write(apps_template.render(app_name=app_name.lower()))
print(f"✅ apps")

# forms
for model in MODELS:
    name = model["name"]

    model_template = Template("""
from django import forms
{% for model in models %}
from {{ app_name }}.models import {{ model.name }}
{% endfor %}
{% for form in forms %}
{% if form.field_select %}
from {{ app_name }}.services.{{ form.field_select.lower() }} import list_{{ form.field_select.lower() }}
{% endif %}
{% endfor %}

{% for form in forms %}
class {{ form.name }}Form(forms.ModelForm):
    class Meta:
        model = {{ form.name }}
        fields = [
        {% for field in form.fields %}
            '{{ field.field }}',
        {% endfor %}
        ]
        widgets = {
            {% for field in form.fields %}
            '{{ field.field }}': forms.{{ field.type }}(attrs={
                'class': 'form-control',
                'placeholder': '{{ field.label }}'
            }),
            {% endfor %}
        }

    {% if form.field_select %}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger les choix dynamiquement
        self.fields['{{ form.field_select }}'].queryset = list_{{ form.field_select.lower() }}()
        # Rendre certains champs optionnels
        self.fields['{{ form.field_select }}'].empty_label = "{{ form.field_select_label }}"
    {% endif %}

{% endfor %}
    """)

    with open(f"generated/{ app_name.lower() }/forms.py", "w") as f:
        f.write(model_template.render(models=MODELS, app_name=app_name.lower(), forms=FORMS))
print(f"✅ forms")


print(f"✅ terminer /generated/{ app_name.lower() }")
