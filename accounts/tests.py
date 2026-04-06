from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AccountsViewsTests(TestCase):
	def test_signup_get_renders(self):
		response = self.client.get(reverse('accounts:signup'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/signup.html')

	def test_signup_post_creates_user_and_logs_in(self):
		response = self.client.post(
			reverse('accounts:signup'),
			data={
				'username': 'newbie',
				'email': 'newbie@example.com',
				'first_name': 'New',
				'last_name': 'User',
				'location': 'Sofia',
				'avatar': 'https://example.com/a.png',
				'bio': 'Hello',
				'password1': 'StrongPass123!',
				'password2': 'StrongPass123!',
			},
			follow=True,
		)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(User.objects.filter(username='newbie').exists())
		self.assertIn('_auth_user_id', self.client.session)
		self.assertTrue(response.context['user'].is_authenticated)

	def test_signup_avatar_must_be_http_url(self):
		response = self.client.post(
			reverse('accounts:signup'),
			data={
				'username': 'badavatar',
				'email': 'badavatar@example.com',
				'avatar': 'not-a-url',
				'password1': 'StrongPass123!',
				'password2': 'StrongPass123!',
			},
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Enter a valid URL.')
		self.assertFalse(User.objects.filter(username='badavatar').exists())

	def test_profile_requires_login(self):
		response = self.client.get(reverse('accounts:profile'))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('accounts:login'), response['Location'])

		user = User.objects.create_user(username='u1', password='StrongPass123!')
		self.client.login(username='u1', password='StrongPass123!')
		response = self.client.get(reverse('accounts:profile'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/profile.html')
