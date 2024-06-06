from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from accounts.models import PatronProfile, CreatorProfile
from patron.models import Tier, TierSubscriptions


class TestPatronViewsMore(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser', password='password')
        self.client.force_login(self.user)
        data = {
            'patron_title': 'TestPatron',
            'bio': 'test user bio',
            'creator_category': 'artist',
        }
        self.response = self.client.post(reverse('create_creator_profile'), data)
        self.creator = CreatorProfile.objects.get(user=self.user)
        # query the view_tiers view
        self.response1 = self.client.get(reverse('patron:tiers'))
        # get tiers
        self.tiers = Tier.objects.filter(creator=self.creator).values()  

    def test_edit_tier_get_request_logged_in(self):
        tier = self.tiers[0] 
        url = reverse('patron:edit_tier', kwargs={'tier_id': tier['id']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patron/admin/actions/edit_tiers.html')

        
    def test_edit_tier_post_request_valid_data(self):
        tier = self.tiers[0] 
        url = reverse('patron:edit_tier', kwargs={'tier_id': tier['id']})
        data = {'name': 'Updated Tier', 'price': 15.00, 'description': 'New description'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        tier = Tier.objects.get(pk=tier['id'])
        self.assertEqual(tier.name, data['name'])
        self.assertEqual(tier.price, data['price'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[2]), 'Tier Edited Successfully.')

    # def test_edit_tier_post_request_invalid_data(self):
    #     tier = self.tiers[0]
    #     print(tier['id'])
    #     url = reverse('patron:edit_tier', kwargs={'tier_id': tier['id']})
    #     data = {'name': 'test', 'price': 'invalid', 'description': 'New description'}
    #     # with self.assertRaises(ValueError):
    #     response = self.client.post(url, data=data)
    #     self.assertEqual(response.status_code, 200)
    #     messages = list(get_messages(response.wsgi_request))
    #     self.assertEqual(str(messages[0]), 'Invalid form. Please check your data.')
        
class TestSubscription(TestCase):
    def setUp(self):
        self.client = Client()
        self.creator_user1 = User.objects.create(
            username='testcreator1', password='password')
        self.creator_user2 = User.objects.create(
            username='testcreator2', password='password')
        self.user1 = User.objects.create(
            username='testuser', password='password')
        self.creator1_obj = CreatorProfile.objects.create(user=self.creator_user1,patron_title='testpatron1', bio='test', creator_category='musician')
        self.creator2_obj = CreatorProfile.objects.create(user=self.creator_user2,patron_title='testpatron2', bio='test', creator_category='musician')
        Tier().create_default_tiers(self.creator1_obj) # creator 1 tiers
        Tier().create_default_tiers(self.creator2_obj) # creator 2 tiers
        self.tiers_1 = Tier.objects.filter(creator=self.creator1_obj).values()
        self.tiers_2 = Tier.objects.filter(creator=self.creator2_obj).values()
        

    def test_join_view_valid(self):
        self.client.force_login(self.user1)
        url = reverse('patron:join_tier', kwargs={'tier_id': self.tiers_1[0]['id']})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Welcome! You Joined my Onetime patrons.")
        self.assertEqual(TierSubscriptions.objects.count(), 1)

    def test_get_creator_patrons(self):
        self.client.force_login(self.creator_user1)
        user1 = User.objects.create(
            username='testuser1', password='password')
        user2 = User.objects.create(
            username='testuser2', password='password')
        user3 = User.objects.create(
            username='testuser3', password='password')
        user4 = User.objects.create(
            username='testuser4', password='password')
        user5 = User.objects.create(
            username='testuser5', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[2]['id'])
        tier3 = Tier.objects.get(pk=self.tiers_2[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)
        TierSubscriptions.objects.create(patron=user2, tier=tier1)
        TierSubscriptions.objects.create(patron=user3, tier=tier2)
        TierSubscriptions.objects.create(patron=user4, tier=tier3)
        TierSubscriptions.objects.create(patron=user5, tier=tier2)
        response = self.client.get(reverse('patron:patrons'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('patron/admin/pages/patrons.html')
        self.assertEqual(TierSubscriptions.objects.count(), 5)


    def test_get_creator_home(self):
        self.client.force_login(self.user1)
        url = reverse('patron:creator_home', kwargs={'creator': self.creator1_obj})
        user1 = User.objects.create(
            username='testuser5', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        TierSubscriptions.objects.create(patron=self.user1, tier=tier1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        

class TestPatronViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser', password='password')
        self.user2 = User.objects.create(
            username='testuser2', password='password')

    def test_choose_profile_type(self):
        url = "choose_profile_type"
        creator_data = {'profile_type': 'creator'}
        patron_data = {'profile_type': 'patron'}
        self.client.force_login(self.user)
        response = self.client.post(reverse(url), creator_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/create/creator")
        response = self.client.post(reverse(url), patron_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/create/patron")

    def test_redirect_unauthenticated_user(self):
        """
        Test that an unathenticated user is redirected to the login page.
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/accounts/profile/")

    def test_profile_redirect(self):
        """
        Test that a user is redirected to choose a profile type
        view, if they don't have one.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/choose")

    def test_create_patron_profile(self):
        """
        Test the creation of a new user.patron_profile
        """
        self.client.force_login(self.user)
        account_number = '77477838'
        city = 'Kitwe'
        data = {'account_number': account_number, 'city': city}
        response = self.client.post(reverse('create_patron_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/")
        self.assertEqual(PatronProfile.objects.count(), 1)
        patron = PatronProfile.objects.get(user=self.user)
        self.assertEqual(patron.account_number, '77477838')
        res = self.client.get(reverse('profile'))
        self.assertEqual(res.status_code, 200)

    def test_create_creator_profile(self):
        """
        Test the creation of a new user.creator_profile
        """
        self.client.force_login(self.user)
        data = {
            'patron_title': 'TestPatron',
            'bio': 'test user bio',
            'creator_category': 'artist',
        }
        response = self.client.post(reverse('create_creator_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/profile/")
        self.assertEqual(CreatorProfile.objects.count(), 1)
        creator = CreatorProfile.objects.get(user=self.user)
        self.assertEqual(creator.patron_title, 'TestPatron')
        res = self.client.get(reverse('profile'))
        self.assertEqual(res.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Your profile data has been saved.")

    def test_create_default_tiers(self):
        """
        Test the creation of a default creator tiers.
        """
        self.client.force_login(self.user)
        data = {
            'patron_title': 'TestPatron',
            'bio': 'test user bio',
            'creator_category': 'artist',
        }
        # create a creator profile
        self.client.post(reverse('create_creator_profile'), data)
        creator = CreatorProfile.objects.get(user=self.user)
        # query the view_tiers view
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        self.assertIn({"name": "Onetime"}, tiers.values('name'))
        self.assertIn({"name": "Fan"}, tiers.values('name'))
        self.assertIn({"name": "Superfan"}, tiers.values('name'))
        self.assertEqual(tiers.count(), 3)
        self.assertEqual(tiers[0]['name'], 'Onetime')
        self.assertEqual(tiers[1]['name'], 'Fan')
        self.assertEqual(tiers[2]['name'], 'Superfan')
        self.assertEqual(tiers[0]['price'], 100)
        self.assertEqual(tiers[1]['price'], 25)
        self.assertEqual(tiers[2]['price'], 50)
        desc = {
            "one": "Make a one-time contribution to support the creator's work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        self.assertEqual(tiers[1]['description'], desc['two'])
        self.assertEqual(tiers[2]['description'], desc['three'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "Default tiers created. Please edit them.")

        response = self.client.get(reverse('patron:tiers'))
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn("Default tiers created. Please edit them.", messages)


    def test_create_default_tiers_different_user_tier_exists(self):
        """
        Test the creation of a default creator tiers.
        """
        data = {
            'patron_title': 'TestPatron',
            'bio': 'test user bio',
            'creator_category': 'artist',
        }
       
        creator1 = CreatorProfile.objects.create(user=self.user,patron_title='testpatron', bio='test', creator_category='musician')
        Tier().create_default_tiers(creator1)
        # login user 2 and create tiers
        self.client.force_login(self.user2)
        self.client.post(reverse('create_creator_profile'), data)
        creator2 = CreatorProfile.objects.get(user=self.user2)
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator2).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        desc = {
            "one": "Make a one-time contribution to support the creator's work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        self.assertEqual(tiers[1]['description'], desc['two'])
        self.assertEqual(tiers[2]['description'], desc['three'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "Default tiers created. Please edit them.")
        

class TestCreateDefaultTiers(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.objects.create(
            username='testuser1', password='password')
        user2 = User.objects.create(
            username='testuser2', password='password')
        self.user3 = User.objects.create(
            username='testuser3', password='password')
        creator1 = CreatorProfile.objects.create(user=user1,patron_title='testpatron1', bio='test', creator_category='musician')
        creator2 = CreatorProfile.objects.create(user=user2,patron_title='testpatron2', bio='test', creator_category='musician')
        Tier().create_default_tiers(creator1)
        Tier().create_default_tiers(creator2)
    
    def test_create_default_tiers_multiple_users_tiers_exists(self):
        """
        Test the creation of a default creator tiers.
        """
        data = {
            'patron_title': 'TestPatron3',
            'bio': 'test user bio',
            'creator_category': 'artist',
        }
       
        # login user 2 and create tiers
        self.client.force_login(self.user3)
        self.client.post(reverse('create_creator_profile'), data)
        creator2 = CreatorProfile.objects.get(user=self.user3)
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator2).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        desc = {
            "one": "Make a one-time contribution to support the creator's work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        self.assertEqual(tiers[1]['description'], desc['two'])
        self.assertEqual(tiers[2]['description'], desc['three'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "Default tiers created. Please edit them.")
