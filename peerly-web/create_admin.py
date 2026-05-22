#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peerly.settings')
django.setup()

from accounts.models import PeerlyUser

# Create superuser
superuser = PeerlyUser.objects.create_superuser(
    email='admin@student.uq.edu.au',
    password='12345678',
    full_name='Admin User'
)
print(f'✓ Superuser created: {superuser.email}')
