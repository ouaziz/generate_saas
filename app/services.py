from apps.{{ app_name }}.models import {{ model_name }}
from django.http import Http404

def list_{{ model_name.lower() }}():
    """Retourne le queryset complet (ou ajoute tes filtres ici)."""
    return {{ model_name }}.objects.all()

def get_{{ model_name.lower() }}(pk):
    try:
        return {{ model_name }}.objects.get(pk=pk)
    except {{ model_name }}.DoesNotExist:
        raise Http404("{{ model_name }} not found")
    except Exception as e:
        raise Http404("{{ model_name }} Error")

def create_{{ model_name.lower() }}(**kwargs):
    try:
        return {{ model_name }}.objects.create(**kwargs)
    except Exception as e:
        raise Http404("{{ model_name }} Error")
    