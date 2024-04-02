from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

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


        
