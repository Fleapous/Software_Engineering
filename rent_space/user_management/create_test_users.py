# create_test_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create test users for testing purposes'

    def handle(self, *args, **options):
        # Create sample users
        users_data = [
            {'username': 'user1', 'password': 'password123'},
            {'username': 'user2', 'password': 'password123'},
            # Add more users as needed
        ]
        for data in users_data:
            username = data['username']
            password = data['password']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password)
        self.stdout.write(self.style.SUCCESS('Sample users created successfully'))
