
from jinja2 import Template

def generate_model(MODELS, app_name):
    model_template = Template("""
from django.db import models
from connexion.models import BaseUUIDModel
from django.contrib.auth.models import User

{% for model in models %}
class {{ model.name }}(BaseUUIDModel):
    {% for name, field in model.fields.items() %}
    {{ name }} = models.{{ field }}
    {% endfor %}

    def __str__(self):
        return self.name
{% endfor %}
    """)

    with open(f"generated/{ app_name.lower() }/models.py", "w") as f:
        f.write(model_template.render(models=MODELS))