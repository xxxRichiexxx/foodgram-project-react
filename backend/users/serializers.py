from rest_framework import serializers
from djoser.serializers import UserSerializer

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField() 

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        try:
            return user.authors.filter(id = obj.id).exists()
        except AttributeError:
            return False

class SubscriptionsSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ('recipes_count', 'recipes',)      

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].GET.get('recipes_limit')
        recipes_list = obj.recipes.all()
        if recipes_limit:
            recipes_list = recipes_list[:int(recipes_limit)]
        return RecipeSerializer(recipes_list, many=True).data