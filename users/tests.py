from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="ugo", email="Ugo@gmail.com").set_password('ugo')

    def test_user_exist(self):
        """user exist"""
        user = User.objects.get(username="ugo")

        self.assertEqual(user.username, 'ugo')
        self.assertEqual(user.email, 'Ugo@gmail.com')
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.balance, 0)
        self.assertEqual(user.photo, "")

