from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User


def create_test_user():
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpassword'

    # Check if user with the specified username already exists
    if not User.objects.filter(username=username).exists():
        # Create the user only if it doesn't exist
        User.objects.create_user(username=username, email=email, password=password)

