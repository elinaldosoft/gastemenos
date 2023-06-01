from django.test import TestCase
from django.contrib.auth.forms import PasswordResetForm


class PasswordResetFormTests(TestCase):
    def test_password_reset_form_valid(self):
        form = PasswordResetForm(data={'email': 'teste@teste.com'})
        self.assertTrue(form.is_valid())

    def test_password_reset_form_invalid(self):
        form = PasswordResetForm(data={'email': 'emailfail'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
