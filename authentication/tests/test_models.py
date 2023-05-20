from rest_framework.test import APITestCase
from authentication.models import User


class TestModel(APITestCase):

    def test_creates_user(self):
        user=User.objects.create_user('admin','admin@gmail.com','admin' )
        self.assertIsInstance(user,User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email,'admin@gmail.com')

    def test_creates_super_user(self):
        user=User.objects.create_user('admin','admin@gmail.com','admin' )
        self.assertIsInstance(user,User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email,'admin@gmail.com')
