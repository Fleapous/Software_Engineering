# create_test_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create test users for testing purposes'

    def handle(self, *args, **options):
        User.objects.create_user(username='user1', email='user1@example.com', password='password1',
                                 contactInfo='123456789')
        User.objects.create_user(username='user2', email='user2@example.com', password='password2',
                                 contactInfo='987654321')

        # Create admin users
        User.objects.create_superuser(username='admin1', email='admin1@example.com', password='adminpassword1',
                                      contactInfo='987654321')
        User.objects.create_superuser(username='admin2', email='admin2@example.com', password='adminpassword2',
                                      contactInfo='123456789')

        self.stdout.write(self.style.SUCCESS('Sample users created successfully'))
