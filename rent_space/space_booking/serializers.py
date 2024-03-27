from .models import AdSpace

# Create operation
from rest_framework import serializers
from .models import AdSpace


class AdSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSpace
        fields = '__all__'

