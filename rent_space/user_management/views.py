from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from .models import User, Log

from .serializers import UserSerializer, UserListSerializer, LogSerializer
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
#from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

# class UserListCreate(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserListCreate(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    @csrf_exempt
    def delete_user(request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
# from serializers import *


# class homeView(APIView):
# def get(selfself, request):
#     output = [{"name": output.email, "email": output.email}
#               for output in User.objects.all()]
#     return Response(output)
#
# def post(self, request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#         return Response(serializer.data)

@csrf_exempt
class homeView(APIView):
    @api_view(['POST'])
    def signup(request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password1')
            confirm_password = request.data.get('password2')  # Assuming you have a field named 'confirm_password'
            email = request.data.get('email')
            # Additional fields as per your User model

            # Check if password and confirm password match
            if password != confirm_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user object
            user = User.objects.create_user(username=username, email=email, password=password)

            if user:
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to create user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    @csrf_exempt
    @api_view(['POST'])
    def custom_login(request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

    @csrf_exempt
    @api_view(['POST'])
    def custom_logout(request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)


class UpdateUser(APIView):
    def put(self, request):
        print(request.data)  # Print request data for debugging

        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)  # Print serializer errors for debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request):
        username = request.query_params.get('username')  # Get username from query parameters
        user = get_object_or_404(User, username=username)  # Fetch user based on username
        serializer = UserSerializer(user)
        return Response(serializer.data)



class LogListCreateView(generics.ListCreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer