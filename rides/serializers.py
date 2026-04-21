from rest_framework import serializers
from .models import Ride, Rating

class RideSerializer(serializers.ModelSerializer):
     rating_by_passenger = serializers.IntegerField(
        source='rating.rating_by_passenger',
        read_only=True
    )
     rating_by_driver = serializers.IntegerField(
        source='rating.rating_by_driver',
        read_only=True
    )
     class Meta:
        model = Ride
        fields = "__all__"
        read_only_fields = ['passenger', 'driver', 'status']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['ride', 'passenger', 'driver']