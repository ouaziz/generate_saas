import os
from django.core.wsgi import get_wsgi_application
from django.db import connection
from datetime import datetime
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_wsgi_application()

# from faker import Faker
# from apps.products.models import Product, ProductBrand, ProductModel, ProductStatus, ProductCategory, ProductType, Company, Warehouse

from django.contrib.auth.models import Group, User, Permission

from tenant.models import Client, Domain, BusinessType, Plan
import uuid
from django_tenants.utils import schema_context


def seed_data_forTenant(business_name):
    with schema_context(business_name):
        # init data
        # os.system("python manage.py tenant_command loaddata fixtures/data/initial_data.json --schema={business_name}")
        # tenant
        print("fixtures/group.json")
        os.system(f"python manage.py tenant_command loaddata fixtures/data/group.json --schema={business_name}")
        print("fixtures/dev/users.json")
        os.system(f"python manage.py tenant_command  loaddata fixtures/dev/users.json --schema={business_name}")
        print("fixtures/dev/profile.json")
        os.system(f"python manage.py tenant_command  loaddata fixtures/dev/profile.json --schema={business_name}")
        
        ## production for IT
        # print("fixtures/data/it/ProductBrand.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/it/ProductBrand.json --schema={business_name}")
        # print("fixtures/data/it/ProductModel.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/it/ProductModel.json --schema={business_name}")
        # print("fixtures/data/it/ProductStatus.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/it/ProductStatus.json --schema={business_name}")
        # print("fixtures/data/it/ProductCategory.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/it/ProductCategory.json --schema={business_name}")
        # print("fixtures/data/it/ProductType.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/it/ProductType.json --schema={business_name}")
        
        # print("fixtures/data/workorder_catagories.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/workorder_catagories.json --schema={business_name}")
        # print("fixtures/data/workorder_status.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/workorder_status.json --schema={business_name}")
        # print("fixtures/data/workorder_cost_catagories.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/workorder_cost_catagories.json --schema={business_name}")
        # print("fixtures/data/workorder_labor_catagories.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/workorder_labor_catagories.json --schema={business_name}")
        # print("fixtures/data/workorder_link_status.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/workorder_link_status.json --schema={business_name}")
        # print("fixtures/data/workorder_task_status.json")
        # os.system(f"python manage.py tenant_command loaddata fixtures/data/workorder_task_status.json --schema={business_name}")
        # ## dev
        # print("fixtures/dev/warehouse.json")
        # os.system(f"python manage.py tenant_command  loaddata fixtures/dev/warehouse.json --schema={business_name}")
        # print("fixtures/dev/company.json")
        # os.system(f"python manage.py tenant_command  loaddata fixtures/dev/company.json --schema={business_name}")
        # print("fixtures/dev/product.json")
        # os.system(f"python manage.py tenant_command  loaddata fixtures/dev/product.json --schema={business_name}")
        # print("fixtures/dev/product_accessory.json")
        # os.system(f"python manage.py tenant_command  loaddata fixtures/dev/product_accessory.json --schema={business_name}")
        ## set permissions to groups
        permissions = Permission.objects.exclude(content_type__app_label__in=["admin","sessions", "tenant"])
        administrator = Group.objects.get(name='Administrator')
        manager = Group.objects.get(name='Manager')
        user = Group.objects.get(name='User')
        support = Group.objects.get(name='Support')
        for permission in permissions:
            administrator.permissions.add(permission)
            if any(action in permission.name for action in ["view", "change", "add"]):
                manager.permissions.add(permission)
            if "view" in permission.name:
                user.permissions.add(permission)
                support.permissions.add(permission)

def delete_all_client_schemas():
    try:
        clients = Client.objects.all()
        with connection.cursor() as cursor:
            for client in clients:
                schema_name = client.schema_name
                print(f"Deleting schema: {schema_name}")
                if schema_name not in ('public', 'pg_toast', 'pg_catalog'):
                    print(f"Drop schema: {schema_name}")
                    cursor.execute(f"DROP SCHEMA {schema_name} CASCADE")
    except Exception as e:
        print(f"Error: {e}")

def seed_and_migrate():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    # reset migrations
    with connection.cursor() as cursor:
        delete_all_client_schemas()
        print(f"Drop schema: Public")
        cursor.execute("DROP SCHEMA public CASCADE;")
        print(f"Create schema: Public")
        cursor.execute("CREATE SCHEMA public;")
    # create tenant

    os.system("python manage.py makemigrations")
    # os.system("python manage.py migrate")
    os.system("python manage.py migrate_schemas --shared")

    os.system("python manage.py delete_tenant -s bigco --noinput")
    os.system("python manage.py delete_tenant -s smallco --noinput")
    os.system("python manage.py delete_tenant -s mediumco --noinput")
    os.system("python manage.py flush")

    # core in public
    print("fixtures/data/language.json")
    os.system(f"python manage.py loaddata fixtures/data/language.json")
    print("fixtures/data/timezone.json")
    os.system(f"python manage.py loaddata fixtures/data/timezone.json")
    print("fixtures/data/currency.json")
    os.system(f"python manage.py loaddata fixtures/data/currency.json")
    print("fixtures/data/plan.json")
    os.system(f"python manage.py loaddata fixtures/data/plan.json")
    print("fixtures/data/business_type.json")
    os.system(f"python manage.py loaddata fixtures/data/business_type.json")

    business_type_instance = BusinessType.objects.get(code="IT")
    plan_instance_free = Plan.objects.get(code="Free")
    plan_instance_basic = Plan.objects.get(code="Basic")

    tenant = Client(schema_name='public', name='public', paid_until='2025-1-1', on_trial=False,
                    business_name='public',
                    start_date=datetime.now().date(),
                    business_type=business_type_instance,
                    plan=plan_instance_free, currency='CAD', language='fr', country='CA')
    tenant.save()
    domain = Domain(domain='lvh.me', tenant=tenant, is_primary=True)
    domain.save()

    # bigco_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, 'bigco.lvh.me')

    # tenant = Client(schema_name='bigco',
    #                 name='bigco',
    #                 business_name='bigco',
    #                 start_date=datetime.now().date(),
    #                 business_type=business_type_instance,
    #                 plan=plan_instance_free, currency='USD', language='en', country='US')
    # tenant.save()
    # domain = Domain(domain='bigco.lvh.me', tenant=tenant, is_primary=True)
    # domain.save()

    tenant = Client(schema_name='smallco',
                    name='smallco',
                    start_date=datetime.now().date(),
                    paid_from=datetime.now().date(),
                    paid_until=datetime.now().date()+ timedelta(days=30),
                    on_trial=False,
                    business_name='smallco',
                    business_type=business_type_instance,
                    plan=plan_instance_basic, currency='CAD', language='fr', country='CA')
    tenant.save()
    domain = Domain(domain='smallco.lvh.me', tenant=tenant, is_primary=True)
    domain.save()

    # tenant = Client(schema_name='mediumco',
    #                 name='mediumco',
    #                 start_date=datetime.now().date(),
    #                 max_trial_days=15,
    #                 on_trial=True,
    #                 business_name='mediumco',
    #                 business_type=business_type_instance,
    #                 plan=plan_instance_basic, currency='USD', language='en', country='CA')
    # tenant.save()
    # domain = Domain(domain='mediumco.lvh.me', tenant=tenant, is_primary=True)
    # domain.save()

    seed_data_forTenant('smallco')
    # seed_data_forTenant('bigco')
    # seed_data_forTenant('mediumco')
    # add admin root
    os.system("python manage.py createsuperuser --username admin --email admin@admin.com")



if __name__ == "__main__":
    seed_and_migrate()