from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class ProfileCreationTest(TestCase):
    def setUp(self):
        self.client= Client()
        User = get_user_model()
        self.staff_user = User.objects.create_user(email='staff', username='teststaff', is_staff=True)
        self.creator_user = User.objects.create_user(email='creator', username='testcreator', has_group=True)
        self.regular_user = User.objects.create_user(email='regular', username='regularuser', password='test')
        self.url = reverse('patron:create_creator_profile')

    def test_redirect_staff_user(self):
        """
        Assert that the user is redirect to the dashboard.
        """
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, '/dashboard/staff/teststaff', 302)


    def test_redirect_creator_user(self):
        """
        Assert that the user is redirect to the dashboard.
        """
        self.client.force_login(self.creator_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, '/patron/accounts/profile/', 302)


    def test_no_redirect_first_time_login(self):
        login = self.client.login(username='regular', password='test')
        self.assertTrue(login)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patron/admin/profile/create_creator_profile.html')

        # user has group
        self.regular_user.has_group = True
        self.regular_user.save()
        response = self.client.get(self.url)
        self.assertRedirects(response, '/patron/accounts/profile/', 302)

        
        

