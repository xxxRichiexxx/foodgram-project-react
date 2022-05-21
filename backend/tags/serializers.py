from rest_framework import serializers

from .models import Tag


class TagSerialiser(serializers.ModelSerializer):
    """Сериалайзер тегов."""
    class Meta:
        model = Tag
        fields = '__all__'
