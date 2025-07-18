
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
{% if form.field_select %}
from apps.{{ app_name }}.services.{{ form.field_select.lower() }}.services import list_{{ form.field_select.lower() }}
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