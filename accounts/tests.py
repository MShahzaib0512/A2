from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import generate_token
from banks.models import Bank

class AccountsViewsTestCase(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        self.user.is_active = True
        self.user.save()
        
        # Create a bank for testing signout
        self.bank = Bank.objects.create(
            name='Test Bank',
            description='Test Bank Description',
            inst_num='123456',
            swift_code='TESTCODE',
            admin=self.user
        )

    def test_accounts_view(self):
        response = self.client.get(reverse('accounts:accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'accounts')

    def test_signup_view_post(self):
        response = self.client.post(reverse('accounts:signup'), {
            'uname': 'newuser',
            'fname': 'New',
            'lname': 'User',
            'email': 'newuser@example.com',
            'pass1': 'newpassword123',
            'pass2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after saving
        self.assertEqual(User.objects.count(), 2)  # Ensure a new user was created
        new_user = User.objects.get(username='newuser')
        self.assertFalse(new_user.is_active)  # User should not be active initially

    def test_signup_view_email(self):
        response = self.client.post(reverse('accounts:signup'), {
            'uname': 'emailtest',
            'fname': 'Email',
            'lname': 'Test',
            'email': 'emailtest@example.com',
            'pass1': 'password123',
            'pass2': 'password123'
        })
        # Check if the email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Confirm your E-mail Address', email.subject)

    def test_signin_view_post(self):
        response = self.client.post(reverse('accounts:signin'), {
            'uname': 'testuser',
            'pass1': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertIn('_auth_user_id', self.client.session)  # Ensure the user is logged in

    def test_signout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('accounts:signout'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)  # Ensure the user is logged out
        self.assertContains(response, 'Test Bank')

    def test_activate_view(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = generate_token.make_token(self.user)
        response = self.client.get(reverse('accounts:activate', args=[uid, token]))
        self.assertEqual(response.status_code, 302)  # Should redirect after activation
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_password_reset_complete_view(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'password_reset_complete')  # Adjust based on actual content

    def test_reset_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('accounts:reset'), {
            'uname': 'testuser',
            'pass1': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful password reset
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_signout_html_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('accounts:signout_html'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Bank')  # Ensure bank data is rendered
