from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe
from django.http.response import Http404
from django.db.models import Q
from utils.recipes.pagination import make_pagination
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 9))


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-created_at')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        })

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={'recipes': page_obj, 'pagination_range': pagination_range, 'title': f'{recipes[0].category.name}'})


def recipes(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'is_detail_page': True,
        'recipe': recipe,
        })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) | Q(description__icontains=search_term),
        is_published=True
    ).order_by('-created_at')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', context={
        'search_term': search_term,
        'page_title': f'Search for "{search_term}"',
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })