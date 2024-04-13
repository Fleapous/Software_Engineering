from .models import AdSpace

# Create operation
from rest_framework import serializers
from .models import AdSpace, Rating


class AdSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSpace
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

