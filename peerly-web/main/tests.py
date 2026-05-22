from django.test import TestCase
from django.urls import reverse

from accounts.models import PeerlyUser

from .models import Classmate, Course


class ClassmatesPageTests(TestCase):
	def setUp(self):
		self.user = PeerlyUser.objects.create(
			email='tester@student.uq.edu.au',
			full_name='Test Student',
		)
		self.user.set_password('safe-password-123')
		self.user.save()
		self.course, _ = Course.objects.get_or_create(
			code='COMS3200',
			defaults={
				'title': 'Computer Communication Networks',
				'enrolled_classmates': 124,
			},
		)
		self.course.classmates.all().delete()
		self.sarah = Classmate.objects.create(
			course=self.course,
			full_name='Sarah Chen',
			degree_name='Bachelor of Computer Science',
			avatar_initials='SC',
			avatar_gradient='linear-gradient(135deg, #9F7AEA 0%, #F6AD55 100%)',
			action_state=Classmate.ActionState.CONNECT,
			display_order=1,
		)
		self.james = Classmate.objects.create(
			course=self.course,
			full_name='James Wilson',
			degree_name='B. Engineering (Honours)',
			avatar_initials='JW',
			avatar_gradient='linear-gradient(135deg, #2D3748 0%, #F6AD55 100%)',
			action_state=Classmate.ActionState.GOING,
			display_order=2,
		)

	def test_classmates_page_requires_login(self):
		response = self.client.get(reverse('classmates'))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('login'), response.url)

	def test_classmates_page_search_filters_results(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse('classmates'), {'q': 'Sarah'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Sarah Chen')
		self.assertNotContains(response, 'James Wilson')

	def test_dashboard_renders_current_user_avatar_initials(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse('home'))
		self.assertContains(response, 'aria-label="Test Student"')
		self.assertContains(response, '<span>TS</span>', html=True)

	def test_campus_events_renders_current_user_avatar_initials(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse('campus-events'))
		self.assertContains(response, 'aria-label="Test Student"')
		self.assertContains(response, '<span>TS</span>', html=True)

	def test_toggle_classmate_status_changes_connect_to_going(self):
		self.client.force_login(self.user)
		response = self.client.post(
			reverse('toggle-classmate-status', args=[self.sarah.id]),
			{'next': reverse('classmates')},
		)
		self.assertRedirects(response, reverse('classmates'))
		self.sarah.refresh_from_db()
		self.assertEqual(self.sarah.action_state, Classmate.ActionState.GOING)

	def test_toggle_classmate_status_changes_going_to_connect(self):
		self.client.force_login(self.user)
		response = self.client.post(
			reverse('toggle-classmate-status', args=[self.james.id]),
			{'next': reverse('classmates')},
		)
		self.assertRedirects(response, reverse('classmates'))
		self.james.refresh_from_db()
		self.assertEqual(self.james.action_state, Classmate.ActionState.CONNECT)
