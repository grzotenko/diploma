from rest_framework import serializers
from .models import *

class FederationBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FederationElement
        fields = ['id', 'title', 'image']

class FederationStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = FederationStaff
        fields = ['id', 'name', 'position', 'image', 'text']