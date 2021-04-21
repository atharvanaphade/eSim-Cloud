from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Delta, DeltaMetadata, State

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['groups']

class DeltaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delta
        fields = ['new_state']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['title']

