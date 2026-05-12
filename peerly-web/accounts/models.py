from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re


def validate_uq_email(value):
    if not re.match(r'^[^@]+@student\.uq\.edu\.au$', value):
        raise ValidationError('Only UQ student email addresses (@student.uq.edu.au) are allowed.')


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

