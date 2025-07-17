# apps/products/forms.py
from django import forms
from apps.products.models import Product
from apps.products.services import list_warehouses, list_companies, list_categories, list_types, list_models, list_status

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'serial_number', 'barcode', 'description', 'image',
            'purchase_date', 'warranty_expiry_date', 'warranty_notes',
            'price', 'status', 'in_stock', 'warehouse', 'company',
            'product_model', 'product_status', 'product_category', 'product_type'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Serial number'
            }),
            'barcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Barcode'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'warranty_expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'warranty_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Warranty notes'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Price'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'in_stock': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'warehouse': forms.Select(attrs={
                'class': 'form-select'
            }),
            'company': forms.Select(attrs={
                'class': 'form-select'
            }),
            'product_model': forms.Select(attrs={
                'class': 'form-select'
            }),
            'product_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'product_category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'product_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger les choix dynamiquement
        self.fields['warehouse'].queryset = list_warehouses()
        self.fields['company'].queryset = list_companies()
        self.fields['product_category'].queryset = list_categories()
        self.fields['product_type'].queryset = list_types()
        self.fields['product_model'].queryset = list_models()
        self.fields['product_status'].queryset = list_status()
        
        # Rendre certains champs optionnels
        self.fields['warehouse'].empty_label = "Select warehouse"
        self.fields['company'].empty_label = "Select company"
        self.fields['product_category'].empty_label = "Select category"
        self.fields['product_type'].empty_label = "Select type"
        self.fields['product_model'].empty_label = "Select model"
        self.fields['product_status'].empty_label = "Select status"