# from rest_framework import serializers
#
# from apps.profile.models import BaseProfile
# from apps.users.serializers import UserSerializer
#
#
# class AdminUserProfileListSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = BaseProfile
#         fields = ['id', 'user', 'username', 'full_name', 'bio', 'image', 'website',
#                   'followers_count', 'following_count', 'posts_count', 'is_private',
#                   'slug', 'created_at', 'updated_at', 'deleted_at']
#
#
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         user_data = rep.pop('user')
#         profile_data = rep
#         return {
#             "user" : user_data,
#             "profile" : profile_data
#         }
#
#
# class AdminProfileCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BaseProfile
#         fields = '__all__'
#
#
# class AdminUserProfileRetrieveUpdateDestroy(serializers.ModelSerializer):
#     class Meta:
#         model = BaseProfile
#         fields = '__all__'
