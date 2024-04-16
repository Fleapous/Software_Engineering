from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import User
from django.urls import reverse
from rest_framework import status
from user_management.serializers import UserSerializer
import json

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')
        self.user.set_password('password123')
        self.user.save()


    def test_custom_login(self):

        user = User.objects.create_user(username='testuser2', password='testpassword')

        response = self.client.post(reverse('login'), {
            'username': 'testuser2',
            'password': 'testpassword',
        })

        self.assertEqual(response.status_code, 200)


        self.assertTrue(response.json()['message'], 'Login successful')


    def test_custom_logout(self):
        self.client.post(reverse('login'), {
            'username': 'testuser2',
            'password': 'testpassword',
        })


        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['message'], 'Logout successful')

    def test_signup(self):

        response = self.client.post(reverse('signup'), {
            'username': 'ttestpuser',
            'email': 'ttestp@example.com',
            'password1': 'password123',
            'password2': 'password123',
        })


        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 201)


        print("User created:", User.objects.filter(username='ttestpuser').exists())
        self.assertTrue(User.objects.filter(username='ttestpuser').exists())


    def test_get_user_profile(self):
        response = self.client.get(reverse('profile') + '?username=test_user')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = UserSerializer(instance=self.user).data
        self.assertEqual(response.data, expected_data)


    def test_update_user(self):
        updated_data = {
            "username": "UPDATED",
            "password": "password123",
            "contactInfo": "updated"
        }
        url = reverse('update_user')
        self.client.force_login(self.user)  # Log in the user
        response = self.client.put(url, data=updated_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, updated_data['username'])
