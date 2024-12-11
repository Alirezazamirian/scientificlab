import hashlib
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from jalali_date import datetime2jalali
from rest_framework.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from scientificlab.settings import DATE_INPUT_FORMATS, TIME_INPUT_FORMATS



RegexValidator(regex=r'^09\d{9}$')


def validate_phone_number(value):
    pattern = r'^09\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('Please enter a valid phone number starting with 09 and having 11 characters.')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone:
            raise ValueError("The given phone must be set")
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.password = make_password(password)
        user.date_joined = datetime2jalali(user.date_joined).strftime(f'{DATE_INPUT_FORMATS} {TIME_INPUT_FORMATS}')
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    last_login = None
    groups = None
    user_permissions = None
    full_name = models.CharField(max_length=100, verbose_name=_("Full name"))
    phone = models.CharField(max_length=11, verbose_name=_("Phone number"), validators=[validate_phone_number],
                             unique=True)
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    is_active = models.BooleanField(default=False, verbose_name=_("Is Active"))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    degree = models.CharField(max_length=50, verbose_name=_("Degree"), null=True, blank=True)
    branch = models.CharField(max_length=50, verbose_name=_("Branch"), null=True, blank=True)
    is_pay = models.BooleanField(default=False, verbose_name=_("Is Pay"))
    pay_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Pay at"))
    donation = models.IntegerField(default=0, verbose_name=_("Donation"))
    donate_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Donate at"))
    hash_identifier = models.CharField(verbose_name=_("Hash identifier"), max_length=72, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return f'{self.phone} --- {self.email} --- {self.full_name}'

    def get_joined_at(self):
        if self.date_joined:
            return datetime2jalali(self.date_joined).strftime(f'{DATE_INPUT_FORMATS} - {TIME_INPUT_FORMATS}')
        return None

    def get_donate_at(self):
        if self.donate_at:
            return datetime2jalali(self.donate_at).strftime(f'{DATE_INPUT_FORMATS} - {TIME_INPUT_FORMATS}')
        return None

    def get_last_login(self):
        if self.last_login:
            return datetime2jalali(self.last_login).strftime(f'{DATE_INPUT_FORMATS} - {TIME_INPUT_FORMATS}')
        return None

    def save(self, *args, **kwargs):
        self.hash_identifier = (hashlib.sha256(self.phone.encode())).hexdigest()
        super().save(*args, **kwargs)

class Code(models.Model):
    verification_code = models.CharField(max_length=10, verbose_name=_("Verification code"), unique=True, null=True,
                                         blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def __str__(self):
        return f'{self.verification_code}'

