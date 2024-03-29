from django.urls import path
from .views import UserListCreate, CreateUserAPIView, update_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('create-user/', CreateUserAPIView.as_view(), name='create-user'),
    path('update/', update_user, name='update_user'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
