from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models
from lipila.models import (
    ContactInfo, HeroInfo, CustomerMessage, UserTestimonial)
from lipila.helpers import (
    get_lipila_contact_info,
    get_user_emails,
    get_lipila_index_page_info,
    get_testimonials,
    get_user_object
)


class HelperFunctionTests(TestCase):
    def test_get_user_object_invalid(self):
        """Test get_user_object returns None"""
        user = 'testuser'
        user_object = get_user_object(user)
        self.assertEqual(user_object, None)

    def test_get_user_object_valid(self):
        """Test get_user_object returns a User object"""
        user = User.objects.create_user('testuser', 'user@email.com', 'testpasss')
        user_object = get_user_object(user)
        self.assertTrue(isinstance(user_object, User))

    def test_get_lipila_contact_info_success(self):
        """Test get_lipila_contact_info returns contact info"""
        ContactInfo.objects.create(
            street="Test Street",
            location="Test Location",
            phone1="123-456-7890",
            email1="test@example.com",
        )
        context = get_lipila_contact_info()
        self.assertIn('contact', context)
        self.assertIsInstance(context['contact'], ContactInfo)

    def test_get_lipila_contact_info_no_data(self):
        """Test get_lipila_contact_info with no ContactInfo"""
        context = get_lipila_contact_info()
        self.assertEqual(context, {'contact': ''})

    def test_get_user_emails(self):
        """Test get_user_emails returns all user emails"""
        CustomerMessage.objects.create(
            name="Test User",
            email="test@user.com",
            subject="Test subject",
            message="Test message",
        )
        context = get_user_emails()
        self.assertIn('user_messages', context)
        self.assertIsInstance(context['user_messages'], models.QuerySet)
        # Test data has 1 email
        self.assertEqual(context['user_messages'].count(), 1)


    def test_get_lipila_index_page_info_success(self):
        """Test get_lipila_index_page_info returns indexpage info"""
        HeroInfo.objects.create(
            message="Test message",
            slogan="Test slogan",
        )  
        context = get_lipila_index_page_info()
        self.assertIn('lipila', context)
        self.assertIsInstance(context['lipila'], HeroInfo)
        self.assertEqual(context['lipila'].message, 'Test message')
        self.assertEqual(context['lipila'].slogan, 'Test slogan')

    def test_get_lipila_index_page_info_no_data(self):
        """Test get_lipila_index_page_info with no HeroInfo"""        
        context = get_lipila_index_page_info()
        self.assertEqual(context, {'lipila': ''})

    def test_get_testimonials(self):
        """Test get_testimonials returns all testimonials"""
        lipila_user = User.objects.create(username="test_user", password="test_password")
        UserTestimonial.objects.create(user=lipila_user
                                   ,message="Test testimonial",
        )
        context = get_testimonials()
        self.assertIn('testimonials', context)
        self.assertIsInstance(context['testimonials'], models.QuerySet)
        # Test data has 1 testimonial
        self.assertEqual(context['testimonials'].count(), 1)
