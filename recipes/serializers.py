from rest_framework import serializers
from .models import Category, Recipe
from tag.models import Tag
from .views import *
from authors.validators import AuthorRecipeValidator

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'category',
            'author',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'preparation_steps_is_html',
            'created_at',
            'updated_at',
            'cover',
            'tags',
            'tags_object',
            'tag_links',
        ]
    category = serializers.StringRelatedField(read_only=True)
    author = serializers.CharField(source='author_full_name', read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    tags_object = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:api_detail_tag',
        read_only=True,
    )

    def validate(self, attrs):
            if self.instance is not None and attrs.get('servings') is None:
                attrs['servings'] = self.instance.servings

            if self.instance is not None and attrs.get('preparation_time') is None:
                attrs['preparation_time'] = self.instance.preparation_time

            super_validate = super().validate(attrs)
            AuthorRecipeValidator(
                data=attrs,
                ErrorClass=serializers.ValidationError,
            )
            return super_validate
