from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
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


class Profile(models.Model):
    """Profile data for a Peerly user."""
    user = models.OneToOneField(PeerlyUser, on_delete=models.CASCADE, related_name='profile')
    headline = models.CharField(max_length=255, default='Passionate about the intersection of ethical AI and modern philosophy.')
    major = models.CharField(max_length=255, default='Computer Science / B. Arts (Philosophy)')
    campus = models.CharField(max_length=255, default='St Lucia Campus')
    joined_at = models.DateField(default=timezone.now)
    about = models.TextField(default='Currently focusing on developing decentralized learning tools for student communities. When I\'m not in the ITEE labs, you can find me at the UQ Philosophy Club or hunting for the best coffee on campus.')
    interests = models.JSONField(default=list)
    connections = models.PositiveIntegerField(default=0)
    active_groups = models.PositiveIntegerField(default=0)
    achievements = models.JSONField(default=list)
    recommended_buddies = models.JSONField(default=list)
    timetable_summary = models.JSONField(default=list)

    def __str__(self):
        return f'{self.user.full_name} Profile'


@receiver(post_save, sender=PeerlyUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            interests=['Ethical AI', 'Full Stack', 'Philosophy of Mind', 'Cybersecurity', 'UX Design'],
            connections=142,
            active_groups=8,
            achievements=[
                {'title': 'Top Mentor', 'subtitle': 'CSSE1001'},
                {'title': 'Hackathon Winner', 'subtitle': 'UQ Hack 2023'},
                {'title': 'Peer Tutor', 'subtitle': 'Silver Tier'},
                {'title': "Dean's List", 'subtitle': 'S2 2023'},
            ],
            recommended_buddies=[
                {'name': 'Sarah Jenkins', 'detail': 'Shared: PHIL1002'},
                {'name': "Liam O'Connor", 'detail': 'Shared: CSSE1001'},
            ],
            timetable_summary=[
                {'day': 'MON', 'time': '10:00 AM - 12:00 PM', 'event': 'CSSE1001 - Lecture', 'location': 'Hawken Eng Building'},
                {'day': 'TUE', 'time': '02:00 PM - 03:00 PM', 'event': 'PHIL1002 - Tutorial', 'location': 'Forgan Smith'},
            ]
        )

