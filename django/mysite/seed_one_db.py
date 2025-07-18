import os
from django.core.wsgi import get_wsgi_application
from django.db import connection
from datetime import datetime
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = get_wsgi_application()

from django.contrib.auth.models import Group, Permission


def seed_data():
    print("fixtures/group.json")
    os.system(f"python manage.py loaddata fixtures/data/group.json")
    print("fixtures/dev/users.json")
    os.system(f"python manage.py loaddata fixtures/dev/users.json")
    print("fixtures/dev/profile.json")
    os.system(f"python manage.py loaddata fixtures/dev/profile.json")
        

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

def seed_and_migrate():
    # delete sqlit3
    os.system("rm db.sqlite3")
    # create sqlit3
    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate")

    seed_data()
    # add admin root
    os.system("python manage.py createsuperuser --username admin --email admin@admin.com")



if __name__ == "__main__":
    seed_and_migrate()