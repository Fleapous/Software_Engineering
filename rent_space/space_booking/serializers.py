# Create operation
from rest_framework import serializers

from .models import AdSpace
from .models import AdSpace, Rating, Booking, Payment
from user_management.serializers import UserSerializer  # Import the UserSerializer

class NotApprovedAdSpaceSerializer(serializers.ModelSerializer):
    ad_space_id = serializers.IntegerField(source='id', read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    username = serializers.CharField(source='owner.username', read_only=True)
    email = serializers.EmailField(source='owner.email', read_only=True)
    first_name = serializers.CharField(source='owner.first_name', read_only=True)
    last_name = serializers.CharField(source='owner.last_name', read_only=True)

    class Meta:
        model = AdSpace
        fields = ['ad_space_id', 'owner_id', 'username', 'email', 'first_name', 'last_name', 'location', 'size', 'price', 'availability', 'isApproved']


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
