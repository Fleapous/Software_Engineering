from django.contrib import admin
from django.contrib.auth.models import User


def create_test_user():
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpassword'

    # Check if user with the specified username already exists
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, email=email, password=password)


class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'method', 'status_code', 'duration', 'timestamp')
    list_filter = ('status_code', 'method')
    search_fields = ('path',)