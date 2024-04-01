from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

def create_test_user():
    username = 'tester'
    email = 'test@test.com'
    password = 'password123'
    User.objects.create_user(username=username, email=email, password=password)


# Call the function to create the user
create_test_user()


