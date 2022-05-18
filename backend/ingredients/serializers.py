from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
	"""Сериалайзер медели ингредиентов."""

	class Meta:
		model = Ingredient
		fields = '__all__'
