from rest_framework import serializers

from apps.banner.models import Banner


class BannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'