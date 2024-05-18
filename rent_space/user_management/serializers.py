# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User

# Create operation
from rest_framework import serializers
from .models import User
from .models import Log


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.contactInfo = validated_data.get('contactInfo', instance.contactInfo)
        instance.save()
        return instance



class UserListSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'contactInfo']


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'