from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from app.accounts.models import User


class PasswordResetViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name="User Teste", email="teste@teste.com",  password='testpassword')

    def test_password_reset(self):
        response = self.client.get(reverse('password_reset'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_password_reset_email_sent(self):
        response = self.client.post(reverse('password_reset'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Django - Registration/Login App Password Reset')

    def test_password_reset_complete(self):
        token = PasswordResetTokenGenerator().make_token(self.user)
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': self.user.pk, 'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_confirm.html')
