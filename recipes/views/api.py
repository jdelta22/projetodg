from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404

@api_view()
def api_list_view(request):
    recipes = Recipe.objects.get_published()[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)
    return Response(serializer.data)


@api_view()
def api_detail_view(request, id):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=id)   
    serializer = RecipeSerializer(instance=recipe, many=False)
    return Response(serializer.data)

