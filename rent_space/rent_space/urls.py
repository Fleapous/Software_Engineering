"""
URL configuration for rent_space project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from user_management.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('testApi.urls')),
    path('signup/', homeView.signup, name='signup'),
    path('api/login/', homeView.custom_login, name='login'),
    path('api/logout/', homeView.custom_logout, name='logout'),
    path('api/', include('space_booking.urls')),  # Include the URLs of your app
    path('logs/', LogListCreateView.as_view(), name='log-list-create'),
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('update_user/<int:user_id>/', UpdateUser.as_view(), name='update_user'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('delete-user/<int:user_id>/', UserListCreate.delete_user, name='delete_user'),
]
