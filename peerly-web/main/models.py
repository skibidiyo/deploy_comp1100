from django.db import models


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
