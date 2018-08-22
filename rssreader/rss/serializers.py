from rest_framework import serializers
from .models import Feed

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ("id", "url")

"""
This serializer allows the Django Rest Framework to
properly transform our Feed Model to JSON, and vice
versa. Using the ModelSerializer allows us to skip most of
the boilerplate, such as explicitly defining each field that
our Model has within the serializer class.
"""
