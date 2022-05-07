from rest_framework import serializers

from .models import Tag


class TagSerialiser(serializers.ModelSerializer):
    
	class Meta:   
		model = Tag
		fields = '__all__'