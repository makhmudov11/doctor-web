from dataclasses import field

from rest_framework import serializers

from apps.banner.models import Banner, BannerChoices
from apps.service.models import Service


class AdminBannerAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class AdminBannerDetailUpdateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Banner
        fields = [
            'image',
            'title',
            'description',
            'url',
            '_type',
            'status'
        ]
        extra_kwargs = {
            'image': {'required': False},
            'title': {'required': False},
            'description': {'required': False},
            'url': {'required': False},
            '_type': {'required': False},
            'status': {'required': False},
        }


class AdminBannerCreateSerializer(serializers.ModelSerializer):
    _type = serializers.ChoiceField(choices=BannerChoices.choices, required=True)
    description = serializers.CharField(required=False, default='')
    url = serializers.URLField(required=False, default='', error_messages={
        'invalid': 'Iltimos, to‘g‘ri URL kiriting.'
    })

    class Meta:
        model = Banner
        fields = [
            'image',
            'title',
            'description',
            'url',
            '_type',
            'status']
        extra_kwargs = {
            "status": {"read_only": True},
            'image': {"required": True},
            'title': {"required": True},
        }


class AdminServiceCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    description = serializers.CharField(required=False, default='')
    class Meta:
        model = Service
        fields = ['name', 'image', 'description']


class AdminServiceAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
