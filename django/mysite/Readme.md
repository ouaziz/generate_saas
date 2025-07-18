# configure

```bash
apt install gettext
apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
# npm install --legacy-peer-deps
yarn
yarn watch
cd ..
python manage.py makemigrations
python manage.py migrate
```

# Seed

```bash
python manage.py seed <application> --number=10
python manage.py seed <application>.<model> --number=10
```

# run

```bash
python3 manage.py runserver
```

# development

## create polls app

```bash
python manage.py startapp <application name>
python manage.py makemigrations
python manage.py makemigrations yourApp
python manage.py migrate
```

## to reset migration

```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```

## Creating an admin user

```bash
python manage.py createsuperuser --username admin --email admin@admin.com
```

## export data simple

```bash
python manage.py dumpdata auth.User --indent 2 > users.json
```
## export tenant data

```bash
python manage.py tenant_command dumpdata products.product --indent 2 > product.json --schema=smallco  
python manage.py tenant_command dumpdata software.software --indent 2 > software.json --schema=smallco
```

# SSL
```bash
sudo apt install mkcert
mkcert -install
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 lvh.me
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem

```

## faker
https://faker.readthedocs.io/en/master/

admin.com

## new app and layout

https://demos.pixinvent.com/materialize-html-admin-template/documentation/django-articles-create-new-page.html

## theme

https://demos.pixinvent.com/materialize-html-admin-template/documentation/django-introduction.html

## postman

https://stackoverflow.com/questions/42754485/how-to-use-postman-to-authenticate-to-django-rest-framework

## JWT

https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html


# Tenants configuration
## first setup
```bash
python manage.py shell
from app.models import Client, Domain
tenant = Client(schema_name='public', name='public', paid_until='2025-12-05', on_trial=False)
tenant.save()

domain = Domain(domain='lvh.me', tenant=tenant, is_primary=True)
domain.save()

tenant = Client(schema_name='tenant1', name='tenant1', paid_until='2025-12-05', on_trial=False)
tenant.save()

domain = Domain(domain='tenant1.lvh.me', tenant=tenant, is_primary=True)
domain.save()
```

## to create example tenant
```bash
python manage.py create_tenant --domain-domain=smallco.lvh.me --schema=smallco --name=smallco 
python manage.py create_tenant --domain-domain=bigco.lvh.me --schema=bigco --name=bigco 
python manage.py create_tenant --domain-domain=hugeco.lvh.me --schema=hugeco --name=hugeco 
```

## if you create a new model
```bash
python manage.py migrate_schemas
```

## MFA
https://www.youtube.com/watch?v=u02U_ZNd0HU
