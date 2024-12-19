# File: Test.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AddUserTestCase(TestCase):
    def setUp(self):
        # Create a test user to log in
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com')
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

        # URL for the AddUser view
        self.add_user_url = reverse('admin_events:list_user')

    def test_add_user_get_request(self):
        # Test GET request to ensure the form is rendered
        response = self.client.get(self.add_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/add_user.html')

    def test_add_user_post_request_valid_data(self):
        # Test POST request with valid data
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        response = self.client.post(self.add_user_url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_add_user_post_request_invalid_data(self):
        # Test POST request with invalid data (e.g., mismatched passwords)
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password456',
        }
        response = self.client.post(self.add_user_url, data)
        self.assertEqual(response.status_code, 200)  # Should stay on the form page
        self.assertFalse(User.objects.filter(username='testuser').exists())
