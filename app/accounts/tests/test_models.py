import uuid

from datetime import datetime

from django.contrib.auth.hashers import check_password
from django.test import TestCase

from app.accounts.models import User


class UserModelTest(TestCase):

    def setUp(self):
        super(UserModelTest, self).setUp()
        self.user = User.objects.create(code=uuid.uuid4(), name="User Teste", email="teste@test.com",  password='testpassword')

    def test_get_user_set_up(self):
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(user.name, "User Teste")
        self.assertEqual(user.email, "teste@test.com")
        self.assertEqual(User.objects.filter().count(), 1)

    def test_create_user(self):
        user = User.objects.create(code=uuid.uuid4(), name="User New", email="teste@usernew.com", password='testnewpassword')
        self.assertTrue(user.id)
        self.assertTrue(user.code)
        self.assertEqual(type(user.code), type(uuid.uuid4()))
        self.assertTrue(check_password('testnewpassword', user.password))
        self.assertEqual(user.name, "User New")
        self.assertEqual(user.email, "teste@usernew.com")
        self.assertEqual(user.created_at.strftime("%Y-%m-%d"), datetime.utcnow().strftime("%Y-%m-%d"))
        self.assertIsNone(user.deleted_at)
        self.assertTrue(user.is_active)
        self.assertIsNone(user.phone)
        self.assertFalse(user.is_superuser)
        self.assertEqual(User.objects.filter().count(), 2)

    def test_user_not_exists(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=-1)
