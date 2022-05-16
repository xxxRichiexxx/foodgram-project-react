from rest_framework import serializers

from .models import Recipe, RecipeIngredients, Ingredient
from tags.serializers import TagSerialiser
from users.serializers import CustomUserSerializer
from .serialaizer_fields import Base64ImageField


class IngredientsGetSerializer(serializers.ModelSerializer):

	name = serializers.CharField(source='ingredient_id.name')
	measurement_unit = serializers.CharField(source='ingredient_id.measurement_unit')
	id = serializers.CharField(source='ingredient_id.id')

	class Meta:
		model = RecipeIngredients
		fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeGetSerialiser(serializers.ModelSerializer):

	tags = TagSerialiser(read_only=True, many=True)
	author = CustomUserSerializer(read_only=True, many=False, source='author_id')
	ingredients = serializers.SerializerMethodField()
	is_favorited = serializers.SerializerMethodField()
	is_in_shopping_cart = serializers.SerializerMethodField()
    
	class Meta:   
		model = Recipe
		exclude = ['author_id']   # Странный момент

	def get_is_favorited(self, obj):
		user = self.context['request'].user
		if user.is_authenticated:
			return user.favorite_recipes.filter(id=obj.id).exists()
		return False

	def get_is_in_shopping_cart(self, obj):
		user = self.context['request'].user
		if user.is_authenticated:
			return user.shopping_list.filter(id=obj.id).exists()
		return False

	def get_ingredients(self, obj):
		ingredients = RecipeIngredients.objects.filter(recipe_id = obj)
		return IngredientsGetSerializer(ingredients, many=True).data


class IngredientCreateSerializer(serializers.ModelSerializer):
	id = serializers.PrimaryKeyRelatedField(
		source='ingredient_id',
		queryset=Ingredient.objects.all(),		
	)

	class Meta:
		model = RecipeIngredients
		fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
	ingredients = IngredientCreateSerializer(many=True, source='recipe_ingredients')
	image = Base64ImageField()

	class Meta:
		model = Recipe
		fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',)
		# exclude = ('author_id', 'date',)
		
	def create(self, validated_data):
		ingredients = validated_data.pop('recipe_ingredients')
		tags = validated_data.pop('tags')
		recipe = Recipe.objects.create(author_id=self.context['request'].user, **validated_data)
		for ingredient in ingredients:
			RecipeIngredients.objects.get_or_create(
				recipe_id = recipe,
                **ingredient,
				)
		for tag in tags:
			recipe.tags.add(tag)
		return recipe

	def update(self, instance, validated_data):
		validated_data['id'] = instance.id
		validated_data['image'] = validated_data.get('image', instance.image)
		instance.delete()
		return self.create(validated_data)		