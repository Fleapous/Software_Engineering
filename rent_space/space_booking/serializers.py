from .models import AdSpace

# Create operation
from rest_framework import serializers
from .models import AdSpace, Rating, Booking


class AdSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSpace
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['client', 'adSpace', 'bookingDate', 'status']

