from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')

    def test_user_creation(self):
        # Test user creation
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'test_user')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_login_view(self):
        # Test login view
        response = self.client.post(reverse('login'), {'username': 'test_user', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)  # Assuming successful login returns status code 200

        # Add more assertions based on your login view's behavior

    # Add more test methods as needed
