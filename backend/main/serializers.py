from rest_framework import serializers

from .models import Recipe, ShoppingList, Ingredient, RecipeIngredients
from tags.serializers import TagSerialiser
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):

	class Meta:
		model = Ingredient
		fields = '__all__'


class RecipeIngredientsSerializer(serializers.ModelSerializer):

	name = serializers.CharField(source='ingredient_id.name')
	measurement_unit = serializers.CharField(source='ingredient_id.measurement_unit')
	id = serializers.CharField(source='ingredient_id.id')

	class Meta:
		model = RecipeIngredients
		fields = ('id', 'name', 'quantity', 'measurement_unit')



class RecipeSerialiser(serializers.ModelSerializer):

	tags = TagSerialiser(read_only=True, many=True)
	author_id = CustomUserSerializer(read_only=True, many=False)
	ingredients = serializers.SerializerMethodField()
	is_favorited = serializers.SerializerMethodField()
	is_in_shopping_cart = serializers.SerializerMethodField()
    
	class Meta:   
		model = Recipe
		fields = '__all__'

	def get_is_favorited(self, obj):
		user = self.context['request'].user
		if user.is_authenticated:
			return user.favorite_recipes.filter(id=obj.id).exists()
		return False

	def get_is_in_shopping_cart(self, obj):
		user = self.context['request'].user
		if user.is_authenticated:
			return obj.ShoppingLists.filter(user_id=user).exists()
		return False

	def get_ingredients(self, obj):
		ingredients = RecipeIngredients.objects.filter(recipe_id = obj)
		return RecipeIngredientsSerializer(instance=ingredients, many=True).data
