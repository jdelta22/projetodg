from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404, get_list_or_404

@api_view(http_method_names=['GET', 'POST'])
def api_list_view(request):
    if request.method == 'GET':        
        recipe = get_list_or_404(Recipe.objects.get_published()[:10])   
        serializer = RecipeSerializer(instance=recipe, many=True ,context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@api_view(http_method_names=['GET', 'PATCH', 'DELETE'])
def api_detail_view(request, id):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=id)   
    if request.method == 'GET':        
        serializer = RecipeSerializer(instance=recipe, many=False,context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = RecipeSerializer(instance=recipe, data=request.data, many=False, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=204)
        
        


@api_view()
def api_detail_tag(request, pk):
    tag = get_object_or_404(Tag.objects.all(), id=pk)
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
