import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('admin', 'Administrator'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    phone_number = PhoneNumberField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)

    def generate_verification_token(self):
        """Generate unique verification token."""
        self.email_verification_token = uuid.uuid4().hex
        self.save()
        return self.email_verification_token

    def verify_email(self, token):
        """Verify email with provided token."""
        if self.email_verification_token == token:
            self.is_email_verified = True
            self.email_verification_token = None
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"