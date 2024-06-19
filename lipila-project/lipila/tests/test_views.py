from django.urls import reverse  # To generate URLs
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
# Custom modules
from patron.models import WithdrawalRequest, ProcessedWithdrawals
from lipila.models import ContactInfo, HeroInfo, UserTestimonial
from lipila.helpers import get_user_object
from lipila.forms.forms import ContactForm
from accounts.models import CreatorProfile


class IndexViewTest(TestCase):
    def setUp(self):
        # Create test data (consider using @skip_unless for helper functions)
        ContactInfo.objects.create(
            street="Test Street",
            location="Test Location",
            phone1="123-456-7890",
            email1="test@example.com",
        )
        HeroInfo.objects.create(
            message="Test message",
            slogan="Test slogan",
        )
        UserTestimonial.objects.create(user=User.objects.create(
            username="test_user"), message="Test testimonial")

    def test_index_view_success(self):
        """Test index view renders successfully with context data"""
        url = reverse('index')  # Generate the URL for the index view
        response = self.client.get(url)

        # Assert HTTP status code
        self.assertEqual(response.status_code, 200)

        # Assert template used
        self.assertTemplateUsed(response, 'index.html')

        # Assert context data (consider using more specific assertions)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertIn('contact', response.context)
        self.assertIn('lipila', response.context)
        self.assertIn('testimony', response.context)


class ContactFormViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_contact_success(self):
        """Test successful contact form submission"""
        valid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message',
        }
        response = self.client.post(reverse('contact'), valid_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(
            str(messages[0]), "Your message has been sent successfully")

    def test_contact_failure(self):
        """Test contact form submission with invalid data"""
        invalid_data = {'message': ''}  # Missing required fields
        response = self.client.post(reverse('contact'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Check form renders again


class ApproveWithdrawalsTest(TestCase):

    def setUp(self):
        # Create a staff user
        self.staff_user = User.objects.create_user(
            username='staffuser', password='staffpassword', is_staff=True)
        self.client = Client()

        # Create a creator user and a withdrawal request
        self.user1 = User.objects.create_user(
            username='creatoruser', password='creatorpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user1, patron_title='testpatron1', bio='test', creator_category='musician')
        self.withdrawal_request = WithdrawalRequest.objects.create(
            creator=self.creator_user,
            amount=100.00,
            account_number='0966445333',
        )

    def test_unauthenticated_access(self):
        # Unauthenticated user should be redirected to login page
        response = self.client.get(reverse('approve_withdrawals'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/approve_withdrawals/')

    def test_non_staff_access(self):
        # Non-staff user should be forbidden
        self.client.force_login(self.user1)
        response = self.client.get(reverse('approve_withdrawals'))
        self.assertEqual(response.status_code, 302)

    def test_staff_access_get(self):
        # Staff user can access the view with a GET request
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('approve_withdrawals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'lipila/staff/approve_withdrawals.html')

    def test_approve_withdrawal(self):
        # Staff user can approve a withdrawal request
        self.client.force_login(self.staff_user)
        data = {
            'withdrawal_request_id': self.withdrawal_request.pk,
            'action': 'approve'
        }
        response = self.client.post(reverse('approve_withdrawals'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('approve_withdrawals'))

        # Check if withdrawal request is updated
        withdrawal_request = WithdrawalRequest.objects.get(
            pk=self.withdrawal_request.pk)
        self.assertEqual(withdrawal_request.status, 'success')

        # Check if processed withdraw is saved
        processed_withdrawal = ProcessedWithdrawals.objects.get(pk=1)
        self.assertEqual(processed_withdrawal.approved_by.username, 'staffuser')
        self.assertEqual(processed_withdrawal.status, 'success')
        

    def test_reject_withdrawal(self):
        # Staff user can reject a withdrawal request
        self.client.force_login(self.staff_user)
        data = {
            'withdrawal_request_id': self.withdrawal_request.pk,
            'action': 'reject',
            'reason': 'Insufficient funds'
        }
        response = self.client.post(reverse('approve_withdrawals'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('approve_withdrawals'))

        # Check if withdrawal request is updated
        withdrawal_request = WithdrawalRequest.objects.get(
            pk=self.withdrawal_request.pk)
        self.assertEqual(withdrawal_request.status, 'rejected')
        self.assertEqual(withdrawal_request.reason, 'Insufficient funds')

        # Check if processed withdraw is saved
        processed_withdrawal = ProcessedWithdrawals.objects.get(withdrawal_request=withdrawal_request)
        self.assertEqual(processed_withdrawal.rejected_by.username, 'staffuser')
        self.assertEqual(processed_withdrawal.status, 'rejected')
        

    def test_invalid_action(self):
        # Staff user submitting an invalid action should display an error message
        self.client.force_login(self.staff_user)
        data = {
            'withdrawal_request_id': self.withdrawal_request.pk,
            'action': 'invalid_action'
        }
        response = self.client.post(reverse('approve_withdrawals'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('approve_withdrawals'))
        # Check for error message in messages (implementation might vary)
        # ... (check for message existence and content)
