from django.db import models
from accounts.models import PeerlyUser


class StudentProfile(models.Model):
	YEAR_CHOICES = [
		('1', 'Year 1'),
		('2', 'Year 2'),
		('3', 'Year 3'),
		('4', 'Year 4'),
		('5', 'Year 5 (Dentistry / Vet)'),
		('honours', 'Honours Year'),
		('pgc', 'Postgraduate Coursework'),
		('phd', 'PhD / MPhil'),
		('international', 'International Student'),
		('double-degree', 'Double Degree'),
	]

	user = models.OneToOneField(PeerlyUser, on_delete=models.CASCADE, related_name='profile')
	degree = models.CharField(max_length=255, blank=True)
	year = models.CharField(max_length=20, choices=YEAR_CHOICES, blank=True)
	bio = models.TextField(max_length=500, blank=True)
	interests = models.JSONField(default=list)
	classes = models.JSONField(default=list)
	birthday = models.DateField(null=True, blank=True)
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


class StudySession(models.Model):
	title = models.CharField(max_length=255)
	course_code = models.CharField(max_length=20)
	location = models.CharField(max_length=255, blank=True)
	scheduled_at = models.DateTimeField()
	host = models.ForeignKey(PeerlyUser, on_delete=models.CASCADE, related_name='hosted_sessions')
	attendees = models.ManyToManyField(PeerlyUser, related_name='joined_sessions', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['scheduled_at']

	def __str__(self):
		return f'{self.title} ({self.course_code})'


class Community(models.Model):
	name = models.CharField(max_length=255)
	category = models.CharField(max_length=100)
	description = models.TextField(max_length=500, blank=True)
	emoji = models.CharField(max_length=10, default='🌟')
	gradient = models.CharField(max_length=120, default='linear-gradient(135deg,#667eea,#764ba2)')
	creator = models.ForeignKey(PeerlyUser, on_delete=models.CASCADE, related_name='created_communities')
	members = models.ManyToManyField(PeerlyUser, through='CommunityMembership', related_name='joined_communities', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.name


class CommunityMembership(models.Model):
	user = models.ForeignKey(PeerlyUser, on_delete=models.CASCADE, related_name='community_memberships')
	community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='memberships')
	joined_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'community')
		ordering = ['-joined_at']

	def __str__(self):
		return f'{self.user.email} → {self.community.name}'


class DiscoverAction(models.Model):
	"""Track likes, passes, and superlikes on the discover page"""
	class ActionType(models.TextChoices):
		PASS = 'pass', 'Pass'
		LIKE = 'like', 'Like'
		SUPERLIKE = 'superlike', 'Superlike'

	user = models.ForeignKey(PeerlyUser, on_delete=models.CASCADE, related_name='discover_actions')
	target_user = models.ForeignKey(PeerlyUser, on_delete=models.CASCADE, related_name='received_actions')
	action_type = models.CharField(max_length=20, choices=ActionType.choices)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'target_user')
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.user.email} {self.action_type} {self.target_user.email}'
