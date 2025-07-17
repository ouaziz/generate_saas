from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from django.urls import reverse_lazy
from django.contrib import messages
from {{ app_name }}.services import list_{{ model_name.lower() }}, get_{{ model_name.lower() }}
from {{ app_name }}.models import {{ model_name }}
from {{ app_name }}.forms import {{ model_name }}Form


class List(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ("{{ app_name }}.view_{{ model_name.lower() }}",)
    template_name = "{{ app_name }}/{{ model_name.lower() }}_list.html"
    context_object_name = "{{ model_name.lower() }}s"

    def get_queryset(self):
        return list_{{ model_name.lower() }}(is_accessory=False)


# class ListJson(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     permission_required = ("{{ app_name }}.view_{{ model_name.lower() }}",)

#     def get(self, request):
#         queryset = list_{{ model_name.lower() }}(is_accessory=False)
#         return standard_list_view(queryset, {{ model_name }}Serializer, request)


class Detail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ("{{ app_name }}.view_{{ model_name.lower() }}",)
    template_name = "{{ app_name }}/{{ model_name.lower() }}_view.html"
    context_object_name = "{{ model_name.lower() }}"

    def get_object(self, queryset=None):
        return get_{{ model_name.lower() }}(self.kwargs["pk"])

class Create(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ("{{ app_name }}.add_{{ model_name.lower() }}",)
    model = {{ model_name }}
    form_class = {{ model_name }}Form
    template_name = "{{ app_name }}/{{ model_name.lower() }}_form.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, '{{ model_name }} created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("{{ model_name.lower() }}-detail", kwargs={"pk": self.object.pk})

class Update(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ("{{ app_name }}.change_{{ model_name.lower() }}",)
    model = {{ model_name }}
    form_class = {{ model_name }}Form
    template_name = "{{ app_name }}/{{ model_name.lower() }}_form.html"
    
    def get_object(self):
        return get_{{ model_name.lower() }}(self.kwargs['pk'])
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, '{{ model_name }} updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("{{ model_name.lower() }}-detail", kwargs={"pk": self.object.pk})

class Delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ("{{ app_name }}.delete_{{ model_name.lower() }}",)
    model = {{ model_name }}
    template_name = "{{ app_name }}/{{ model_name.lower() }}_confirm_delete.html"
    success_url = reverse_lazy("{{ model_name.lower() }}-list")
    
    def get_object(self):
        return get_{{ model_name.lower() }}(self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '{{ model_name }} deleted successfully!')
        return super().delete(request, *args, **kwargs)