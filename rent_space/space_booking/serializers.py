# Create operation
from rest_framework import serializers

from .models import AdSpace
from .models import AdSpace, Rating, Booking, Payment
from user_management.serializers import UserSerializer  # Import the UserSerializer


class NotApprovedAdSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSpace
        fields = ['id', 'location', 'size', 'price', 'owner_id']


class AdSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSpace
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['client', 'adSpace', 'bookingDate', 'status']


class BookingDetailSerializer(serializers.ModelSerializer):
    adSpace = AdSpaceSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'adSpace', 'bookingDate', 'status']
