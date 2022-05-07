from rest_framework import serializers
from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    def get_is_subscribed(self, obj):
        return obj.authors.filter(id = self.context.get('request').user.id).exists()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)