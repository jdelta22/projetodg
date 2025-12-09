from rest_framework import serializers
from .models import Category

class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=165)
    description = serializers.CharField(max_length=165)
    preparation_time = serializers.IntegerField()
    preparation_time_unit = serializers.CharField(max_length=65)
    servings = serializers.IntegerField()
    servings_unit = serializers.CharField(max_length=65)
    preparation_steps = serializers.CharField()
    preparation_steps_is_html = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    cover = serializers.ImageField()
    category = serializers.StringRelatedField()
    author = serializers.CharField(source='author_full_name')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')


