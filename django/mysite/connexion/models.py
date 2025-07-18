from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class BaseUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True
# from django_countries.fields import CountryField
# from localflavor.ca.forms import CAPostalCodeField
# from phonenumber_field.modelfields import PhoneNumberField

# from django.contrib.auth import get_user_model

# User = get_user_model()

# class UserActivityLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)  
#     action = models.CharField(max_length=255)
#     url = models.CharField(max_length=255)
#     method = models.CharField(max_length=10)
#     ip_address = models.GenericIPAddressField()

#     # Device and browser info
#     device_type = models.CharField(max_length=50, null=True, blank=True)
#     browser = models.CharField(max_length=50, null=True, blank=True)
#     browser_version = models.CharField(max_length=50, null=True, blank=True)
#     os = models.CharField(max_length=50, null=True, blank=True)

#     # Location info
#     country = models.CharField(max_length=100, null=True, blank=True)
#     city = models.CharField(max_length=100, null=True, blank=True)
#     latitude = models.FloatField(null=True, blank=True)
#     longitude = models.FloatField(null=True, blank=True)

#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-timestamp']

#     def __str__(self):
#         return f"{self.user.username} - {self.action} - {self.timestamp}"

class Department(BaseUUIDModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Profile(BaseUUIDModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    email_token = models.CharField(max_length=100, blank=True, null=True)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    contract_type = models.CharField(max_length=100, blank=True, null=True)
    join_date = models.DateField(null=True, blank=True)
    leave_date = models.DateField(null=True, blank=True)
    manager = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    mfa_secret = models.CharField(max_length=100, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    # @receiver(post_save, sender=User)
    # def create_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)


    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
