from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
    # @api_view(['POST'])
    # def signup(request):
    #     if request.method == 'POST':
    #         form = UserCreationForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return Response({'message': 'User created successfully'}, status=201)
    #         else:
    #             return Response({'errors': form.errors}, status=400)
    #     else:
    #         return Response({'message': 'Method not allowed'}, status=405)

    @api_view(['POST'])
    def signup(request):
        if request.method == 'POST':
            form = UserCreationForm(request.data)
            if form.is_valid():
                form.save()
                return Response({'message': 'User created successfully'}, status=201)
            else:
                return Response({'errors': form.errors}, status=400)
        else:
            return Response({'message': 'Method not allowed'}, status=405)

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

    @api_view(['POST'])
    def custom_logout(request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)


class UpdateUser(APIView):
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)  # Log the user in after successful login
#             return JsonResponse({'message': 'Login successful'}, status=200)
#         else:
#             return JsonResponse({'errors': form.errors}, status=400)
#     else:
#         return JsonResponse({'message': 'Method not allowed'}, status=405)
