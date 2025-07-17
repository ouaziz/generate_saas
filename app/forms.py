# apps/products/forms.py
from django import forms
from {{ app_name }}.models import {{ model_name }}
from {{ app_name }}.services.{{ field_select.lower() }} import list_{{ field_select.lower() }}

class {{ model_name }}Form(forms.ModelForm):
    class Meta:
        model = {{ model_name }}
        fields = [
            '{{ fields }}',
        ]
        widgets = {
            '{{ field }}': forms.{{ type }}(attrs={
                'class': 'form-control',
                'placeholder': '{{ label }}'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger les choix dynamiquement
        self.fields['{{ field_select }}'].queryset = list_{{ field_select.lower() }}()
        # Rendre certains champs optionnels
        self.fields['{{ field_select }}'].empty_label = "{{ field_select_label }}"