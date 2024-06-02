from django.contrib.admin import AdminSite
from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client

from .admin import LogAdmin
from .models import User, Log
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from user_management.serializers import UserSerializer
from rest_framework.test import APIClient
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

    def test_delete_user(self):
        user_id = self.user.id
        response = self.client.delete(reverse('delete_user', args=[user_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_delete_nonexistent_user(self):
        response = self.client.delete(reverse('delete_user', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='john_doe', first_name='John', last_name='Doe', email='john.doe@example.com', date_joined='2021-06-21', contactInfo='+123456789')
        self.user2 = User.objects.create(username='jane_smith', first_name='Jane', last_name='Smith', email='jane.smith@example.com', date_joined='2022-08-18', contactInfo='+987654321')

    def test_user_list(self):
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.count())


class LogModelTest(TestCase):

    def setUp(self):
        self.log = Log.objects.create(
            path='/api/endpoint1',
            method='GET',
            status_code=200,
            duration=0.5,
            timestamp=timezone.now()
        )

    def test_log_creation(self):
        self.assertIsInstance(self.log, Log)
        self.assertEqual(self.log.path, '/api/endpoint1')
        self.assertEqual(self.log.method, 'GET')
        self.assertEqual(self.log.status_code, 200)
        self.assertEqual(self.log.duration, 0.5)
        self.assertIsNotNone(self.log.timestamp)

    def test_str_method(self):
        self.assertEqual(str(self.log), f"{self.log.method} {self.log.path} - {self.log.status_code}")


class LogAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.log_admin = LogAdmin(Log, self.site)
        self.log = Log.objects.create(
            path='/api/endpoint1',
            method='GET',
            status_code=200,
            duration=0.5,
            timestamp=timezone.now()
        )

    def test_list_display(self):
        self.assertEqual(
            self.log_admin.list_display,
            ('id', 'path', 'method', 'status_code', 'duration', 'timestamp')
        )

    def test_list_filter(self):
        self.assertEqual(
            self.log_admin.list_filter,
            ('status_code', 'method')
        )

    def test_search_fields(self):
        self.assertEqual(
            self.log_admin.search_fields,
            ('path',)
        )


class LoggingMiddlewareTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_logging_get_request(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 405)

        log = Log.objects.last()
        self.assertIsNotNone(log)
        self.assertEqual(log.path, reverse('signup'))
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.status_code, 405)

    def test_logging_post_request(self):
        response = self.client.post(reverse('signup'), data={
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 201)  # User creation should return 201

        log = Log.objects.last()
        self.assertIsNotNone(log)
        self.assertEqual(log.path, reverse('signup'))
        self.assertEqual(log.method, 'POST')
        self.assertEqual(log.status_code, 201)