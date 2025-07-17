# apps/products/services.py
from apps.products.models import Product, Warehouse, Company, ProductCategory, ProductType, ProductBrand, ProductModel, ProductStatus
from django.shortcuts import get_object_or_404
from django.http import Http404

def list_products(is_accessory=False):
    """Retourne le queryset complet (ou ajoute tes filtres ici)."""
    return Product.objects.filter(is_accessory=is_accessory)

def get_product(pk):
    # return get_object_or_404(Product, pk=pk)
    try:
        return Product.objects.select_related(
            'warehouse',
            'company', 
            'product_category',
            'product_type',
            'product_model',
            'product_status',
            'user'  # if you want user info too
        ).get(pk=pk)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    except Exception as e:
        raise Http404("Product Error")

def create_product(product):
    return Product.objects.create(**product)

def list_warehouses():
    return Warehouse.objects.filter(status=True)
    
def list_companies():
    return Company.objects.filter(status=True)
    
def list_categories():
    return ProductCategory.objects.filter(status=True)

def list_all_categories():
    return ProductCategory.objects.all()

def get_category(pk):
    try:
        return ProductCategory.objects.get(pk=pk)
    except ProductCategory.DoesNotExist:
        raise Http404("Category not found")
    except Exception:
        raise Http404("Category Error")
    
def list_types():
    return ProductType.objects.filter(status=True)
    
def list_brands():
    return ProductBrand.objects.filter(status=True)

def list_all_brands():
    return ProductBrand.objects.all()

def get_brand(pk):
    try:
        return ProductBrand.objects.get(pk=pk)
    except ProductBrand.DoesNotExist:
        raise Http404("Brand not found")
    except Exception as e:
        raise Http404("Brand Error")

def list_models():
    return ProductModel.objects.filter(status=True)

def get_model(pk):
    try:
        return ProductModel.objects.get(pk=pk)
    except ProductModel.DoesNotExist:
        raise Http404("Model not found")
    except Exception as e:
        raise Http404("Model Error")
def list_status():
    return ProductStatus.objects.filter(status=True)

def get_status(pk):
    try:
        return ProductStatus.objects.get(pk=pk)
    except ProductStatus.DoesNotExist:
        raise Http404("Status not found")
    except Exception as e:
        raise Http404("Status Error")