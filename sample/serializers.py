from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import CookBook, Recipe


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'follows',
            'followed_by',
        )


class CookBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = CookBook
        fields = (
            'id',
            'user',
            'name',
            'slug',
            'likes',
            'recipes',
        )


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'cookbook',
            'title',
            'body',
            'likes',
        )
