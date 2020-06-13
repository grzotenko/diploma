from rest_framework import serializers
from .models import *

class FederationBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FederationElement
        fields = ['id', 'title',]

class FederationStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = FederationStaff
        fields = ['id', 'name', 'position', 'image', 'text']

class FederationElementSerializer(serializers.ModelSerializer):
    federationstaff_set = FederationStaffSerializer(many = True)

    class Meta:
        model = FederationElement
        fields = ['id', 'title', 'federationstaff_set']

class FederationSerializer(serializers.ModelSerializer):
    federationelement_set = FederationElementSerializer(many = True)

    class Meta:
        model = Federation
        fields = ['work_time', 'text', 'email', 'phone', 'map', 'address', 'federationelement_set']