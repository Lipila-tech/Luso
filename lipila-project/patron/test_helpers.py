from django.test import TestCase
from django.contrib.auth.models import User

# custom modules
from patron import helpers
from accounts.models import CreatorProfile, PatronProfile


class HelperFunctionTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='testpass')
        self.user2 = User.objects.create(username='user2', password='testpass')
        self.user3 = User.objects.create(username='user3', password='testpass')

    def test_get_patrons_no_patrons(self):
        """raises an exception no patron objects exists"""
        with self.assertRaises(helpers.NoPatronsFoundError):
            helpers.get_patrons()

    def test_get_patrons_with_patrons(self):
        PatronProfile.objects.create(user=self.user1)
        PatronProfile.objects.create(user=self.user2)
        PatronProfile.objects.create(user=self.user3)
        all_patrons = helpers.get_patrons()
        self.assertEqual(len(all_patrons), 3)
        

    def test_get_creators_no_creators(self):
        """raises NoCreatorsFoundError"""
        with self.assertRaises(helpers.NoCreatorsFoundError):
            helpers.get_creators()

    def test_get_creators_with_creators(self):
        """returns a list of 2 creator objects"""
        CreatorProfile.objects.create(user=self.user1)
        CreatorProfile.objects.create(user=self.user2)
        all_creators = helpers.get_creators()
        self.assertEqual(len(all_creators), 2)

    def test_get_patron_or_creator(self):
        CreatorProfile.objects.create(user=self.user2)
        PatronProfile.objects.create(user=self.user1)
        p1 = helpers.get_patron_or_creator(self.user1)
        p2 = helpers.get_patron_or_creator(self.user2)
        p3 = helpers.get_patron_or_creator(self.user3)
        self.assertTrue(isinstance(p1, PatronProfile), True)
        self.assertTrue(isinstance(p2, CreatorProfile), True)
        self.assertFalse(isinstance(p3, CreatorProfile), True)
        self.assertFalse(isinstance(p3, PatronProfile), True)
        self.assertTrue(isinstance(p3, User), True)
        with self.assertRaises(User.DoesNotExist):
            p4 = helpers.get_patron_or_creator(1)