from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
import re


def validate_uq_email(value):
    if not re.match(r'^[^@]+@student\.uq\.edu\.au$', value):
        raise ValidationError('Only UQ student email addresses (@student.uq.edu.au) are allowed.')


class PeerlyUserManager(BaseUserManager):
    """Custom manager for PeerlyUser model."""
    
    def create_user(self, email, password=None, full_name='', **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, full_name='', **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, full_name, **extra_fields)


class PeerlyUser(AbstractUser):
    """Custom user model for Peerly — restricted to UQ email addresses."""
    username = None  # Remove username field; use email as identifier
    full_name = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True,
        validators=[validate_uq_email],
        help_text='Must be a UQ email address (@uq.net.au or @student.uq.edu.au).'
    )
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PeerlyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name


