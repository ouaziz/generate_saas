
from jinja2 import Template

def generate_forms(app_name, MODELS, FORMS):
    for model in MODELS:
        name = model["name"]

        model_template = Template("""
from django import forms
{% for model in models %}
from apps.{{ app_name }}.models import {{ model.name }}
{% endfor %}
{% for form in forms %}
{% if form.selects %}
{% for select in form.selects %}
from apps.{{ app_name }}.services.{{ select.name.split(",")[0].lower() }}.services import list_{{ select.name.split(",")[0].lower() }}
{% endfor %}
{% endif %}
{% endfor %}

{% for form in forms %}
class {{ form.name }}Form(forms.ModelForm):
    class Meta:
        model = {{ form.name }}
        fields = [
        {% for f in form.fields %}
            '{{ f.field.split(",")[0] }}',
        {% endfor %}
        ]
        widgets = {
            {% for f in form.fields %}
            '{{ f.field.split(",")[0] }}': forms.{{ f.field.split(",")[1] }}(attrs={
                'class': 'form-control',
                'placeholder': '{{ f.field.split(",")[2] }}'
            }),
            {% endfor %}
        }

    {% if form.selects %}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger les choix dynamiquement
        {% for select in form.selects %}
        self.fields['{{ select.name.split(",")[0] }}'].queryset = list_{{ select.name.split(",")[0].lower() }}()
        {% endfor %}
        # Rendre certains champs optionnels
        {% for select in form.selects %}
        self.fields['{{ select.name.split(",")[0] }}'].empty_label = "{{ select.name.split(",")[1] }}"
        {% endfor %}
    {% endif %}

{% endfor %}
        """)

        with open(f"generated/{ app_name.lower() }/forms.py", "w") as f:
            f.write(model_template.render(models=MODELS, app_name=app_name.lower(), forms=FORMS))