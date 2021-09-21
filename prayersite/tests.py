from django.test import TestCase
from account.models import Profile
from account.models import AccountSettings

from django.contrib.auth.models import User

class UserModelTests(TestCase):
    def test_user_creation(self):
        t = User.objects.create_user('testuser', 'testuser@bastelli.net', 'testuserpassword')
        self.assertEquals(len(User.objects.filter(username='testuser')),1)
    def test_user_profile_creation(self):
        t = User.objects.create_user('testuser', 'testuser@bastelli.net', 'testuserpassword')
        self.assertTrue(type(t.profile) == Profile)
    def test_user_account_settings_creation(self):
        t = User.objects.create_user('testuser', 'testuser@bastelli.net', 'testuserpassword')
        self.assertTrue(type(t.settings) == AccountSettings)
