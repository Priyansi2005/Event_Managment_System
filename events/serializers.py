from rest_framework import serializers
from .models import Event, RSVP, Review

class RSVPSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RSVP
        fields = ['id', 'user', 'status']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment']

class EventSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    rsvps = RSVPSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'owner', 'rsvps', 'reviews']
