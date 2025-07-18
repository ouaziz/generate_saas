import json
import os
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import shutil
from forms import generate_forms
from templates import generate_template

def copy_init_file(path):
    shutil.copy("app/__init__.py", f"{ path }/__init__.py")

def clean_folder(schema_name):
    # remove folder
    if os.path.exists(f"generated/{ schema_name }"):
        shutil.rmtree(f"generated/{ schema_name }")
    print(f"✅ cleaning folder {schema_name}")
    
def generate(schema_name):
    with open(schema_name) as f:
        schema = json.load(f)
    print(f"✅ reading {schema_name}")

    PROJECT_NAME = schema["project"]
    MODELS = schema["models"]
    TEMPLATES = schema["templates"]
    FORMS = schema["forms"]

    app_name = schema["app_name"]
    os.makedirs(f"generated/{ app_name }", exist_ok=True)
    copy_init_file(f"generated/{ app_name }")

    # # ==== templates list =======#
    generate_template(app_name, TEMPLATES)
    print(f"✅ templates list")

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
    copy_init_file(f"generated/{ app_name.lower() }")
    print(f"✅ models")

    # === serializers.py ===
    for model in MODELS:
        name = model["name"]
        os.makedirs(f"generated/{ app_name.lower() }/views/{name.lower()}/api", exist_ok=True)
        copy_init_file(f"generated/{ app_name.lower() }/views/{name.lower()}/api")
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
        copy_init_file(f"generated/{ app_name.lower() }/views/{name.lower()}/api")
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
        copy_init_file(f"generated/{ app_name.lower() }/views/{name.lower()}/html")
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
        copy_init_file(f"generated/{ app_name.lower() }/services/{name.lower()}")
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
        copy_init_file(f"generated/{ app_name.lower() }/urls/{name.lower()}/api")
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
        copy_init_file(f"generated/{ app_name.lower() }/urls/{name.lower()}/html")
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
    generate_forms(app_name, MODELS, FORMS)
    print(f"✅ forms")
    print(f"✅ terminer /generated/{ app_name.lower() }")


# i want to give the name f schema in a prompt
if __name__ == "__main__":
    schema_name = input("Enter the schema name: ")
    if not schema_name.endswith(".json"):
        schema_name += ".json"
    if not os.path.exists(schema_name):
        print(f"❌ schema {schema_name} not found")
        exit(1)
    clean_folder(schema_name)
    generate(schema_name)