from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from serializers import UserSerializer

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')

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
            'username': 'testuser',
            'email': 'testemail@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })

       
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 201)

        
        print("User created:", User.objects.filter(username='testuser').exists())
        self.assertTrue(User.objects.filter(username='testuser').exists())


    def test_update_user(self):
        # Define the data to be updated
        updated_data = {'username': 'updated_username', 'email': 'updated@example.com'}

        # Make a PUT request to update the user
        response = self.client.put(reverse('update_user', kwargs={'pk': self.user.pk}), data=updated_data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user data has been updated correctly
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_username')
        self.assertEqual(self.user.email, 'updated@example.com')


    def test_get_user_profile(self):
        # Make a GET request to fetch the user profile
        response = self.client.get(reverse('user_profile', kwargs={'pk': self.user.pk}))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the user's data
        expected_data = UserSerializer(instance=self.user).data
        self.assertEqual(response.data, expected_data)

