from rest_framework import serializers

from apps.banner.models import Banner, BannerChoices
from apps.service.models import Service

class AdminBannerAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class AdminBannerCreateSerializer(serializers.ModelSerializer):
    _type = serializers.ChoiceField(choices=BannerChoices.choices)
    class Meta:
        model = Banner
        fields = [
            'title',
            'description',
            'url',
            '_type',
            'status']

class AdminServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'image', 'description']

class AdminServiceAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
