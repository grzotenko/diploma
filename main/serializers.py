from rest_framework import serializers
from .models import Partner,Contact, Main, SocialNet,Menu
class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = ['banner', 'logo','copyright']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title', 'path']

class PartnersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'url', 'image']


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['title', 'phone', 'email', 'address', 'map']


class SocialNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNet
        fields = ['vk', 'instagram', 'youtube', 'facebook']

class CommonSerializer(serializers.Serializer):
    main = MainSerializer()
    menu = MenuSerializer(many=True)
    social = SocialNetSerializer()
    partners = PartnersSerializer(many=True)
    contacts = ContactsSerializer()
    massMedia = ContactsSerializer()

