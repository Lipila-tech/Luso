from django.test import TestCase
from django.contrib.auth.models import User

# custom modules
from patron import helpers
from patron.models import CreatorUser, PatronUser


class HelperFunctionTests(TestCase):
    # def setUp(self):
    #     self.user1 = User.objects.create(username='user1', password='testpass')
    #     self.user2 = User.objects.create(username='user2', password='testpass')
    #     self.user3 = User.objects.create(username='user3', password='testpass')

    def test_get_patrons_none(self):
        """raises an exception no patron objects exists"""
        with self.assertRaises(helpers.NoPatronsFoundError):
            helpers.get_patrons()

    def test_get_patrons_present(self):
        """returns a list of 3 patron objects"""
        user1 = User(username='user1', password='testpass')
        user2 = User.objects.create(username='user2', password='testpass')
        user3 = User.objects.create(username='user3', password='testpass')
        patron = PatronUser.objects.create()
        patron.user = user1
        patron.save()
        # PatronUser(user=user2)
        # PatronUser(user=user3)
        all_patrons = helpers.get_patrons()
        self.assertEqual(len(all_patrons), 3)

    def test_get_creators_none(self):
        """raises NoCreatorsFoundError"""
        with self.assertRaises(helpers.NoCreatorsFoundError):
            helpers.get_creators()

    def test_get_creators_present(self):
        """returns a list of 2 creator objects"""
        creator1 = CreatorUser(user=self.user1)
        creator2 = CreatorUser(user=self.user2)
        all_creators = helpers.get_creators()
        self.assertEqual(len(all_creators), 2)


