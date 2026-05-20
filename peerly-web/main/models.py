from django.db import models
from accounts.models import PeerlyUser


class StudentProfile(models.Model):
	YEAR_CHOICES = [
		('1', '1st Year'),
		('2', '2nd Year'),
		('3', '3rd Year'),
		('4', '4th Year'),
		('5', '5th Year'),
		('postgrad', 'Postgraduate'),
	]

	user = models.OneToOneField(PeerlyUser, on_delete=models.CASCADE, related_name='profile')
	degree = models.CharField(max_length=255, blank=True)
	year = models.CharField(max_length=20, choices=YEAR_CHOICES, blank=True)
	bio = models.TextField(max_length=500, blank=True)
	interests = models.JSONField(default=list)
	classes = models.JSONField(default=list)
	profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.user.email} Profile'


class Course(models.Model):
	code = models.CharField(max_length=20, unique=True)
	title = models.CharField(max_length=255)
	enrolled_classmates = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['code']

	def __str__(self):
		return f'{self.code} — {self.title}'


class Classmate(models.Model):
	class ActionState(models.TextChoices):
		CONNECT = 'connect', 'Connect'
		GOING = 'going', 'Going'

	course = models.ForeignKey(Course, related_name='classmates', on_delete=models.CASCADE)
	full_name = models.CharField(max_length=255)
	degree_name = models.CharField(max_length=255)
	avatar_initials = models.CharField(max_length=4)
	avatar_gradient = models.CharField(max_length=120)
	accent_color = models.CharField(max_length=20, default='#7C3AED')
	is_online = models.BooleanField(default=False)
	action_state = models.CharField(max_length=20, choices=ActionState.choices, default=ActionState.CONNECT)
	display_order = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['display_order', 'full_name']

	def __str__(self):
		return f'{self.full_name} ({self.course.code})'
