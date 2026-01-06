from rest_framework import serializers
from apps.service.models import SocialNetwork

class SocialNetworkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = '__all__'