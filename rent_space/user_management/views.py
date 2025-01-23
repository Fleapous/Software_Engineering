from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from .models import User, Log
from .serializers import UserSerializer, UserListSerializer, LogSerializer
from django.http import JsonResponse
from django.contrib.auth import logout, authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt


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


@csrf_exempt
class homeView(APIView):
    @api_view(['POST'])
    def signup(request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password1')
            confirm_password = request.data.get('password2')
            email = request.data.get('email')

            # Check if password and confirm password match
            if password != confirm_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

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
                return JsonResponse({
                    'username': user.username,
                    'id': user.id,
                    'is_staff': user.is_staff,
                }, status=200)
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

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)



class LogListCreateView(generics.ListCreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer