from rest_framework import serializers

from tags.serializers import TagSerialiser
from users.serializers import CustomUserSerializer

from .models import Ingredient, Recipe, RecipeIngredients
from .serialaizer_fields import Base64ImageField


class IngredientsGetSerializer(serializers.ModelSerializer):
    """Вложенный сериалайзер для отражения ингредиентов в разрезе рецепта."""
    name = serializers.CharField(
        source='ingredient_id.name',
    )
    measurement_unit = serializers.CharField(
        source='ingredient_id.measurement_unit',
    )
    id = serializers.CharField(source='ingredient_id.id')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeGetSerialiser(serializers.ModelSerializer):
    """Сериалайзер для чтения рецептов."""
    tags = TagSerialiser(read_only=True, many=True)
    author = CustomUserSerializer(
        read_only=True,
        many=False,
        source='author_id',
    )
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ['author_id']

    @staticmethod
    def get_ingredients(obj):
        ingredients = obj.recipe_ingredients.all()
        return IngredientsGetSerializer(ingredients, many=True).data


class IngredientCreateSerializer(serializers.ModelSerializer):
    """
    Вложенный сериализатор для десериализации ингредиентов
    при создании рецепта.
    """
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient_id',
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания рецептов."""
    ingredients = IngredientCreateSerializer(
        many=True,
        source='recipe_ingredients'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('author_id', 'date',)

    @staticmethod
    def add_ingredients(recipe, ingredients):
        for ingredient in ingredients:
            RecipeIngredients.objects.get_or_create(
                recipe_id=recipe,
                **ingredient,
            )
        return recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        validated_data['author_id'] = self.context['request'].user
        recipe = super().create(validated_data)
        return self.add_ingredients(recipe, ingredients)

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        validated_data['image'] = validated_data.get('image', instance.image)
        recipe = super().update(instance, validated_data)
        recipe.ingredients.clear()
        return self.add_ingredients(recipe, ingredients)
