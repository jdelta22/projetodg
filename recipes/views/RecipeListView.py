from ..models import Recipe
from utils.recipes.pagination import make_pagination
from django.views.generic import ListView
import os
from django.db.models import Q


PER_PAGE = int(os.environ.get('PER_PAGE', 9))

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/pages/home.html"
    context_object_name = "recipes"
    ordering= ['-created_at']
    paginate_by = None

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs 

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context['recipes'],
            PER_PAGE)
        
        context.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
        })
        return context 
    
class RecipeListViewHome(RecipeListView):
    template_name = "recipes/pages/home.html"
    


class RecipeListViewCategory(RecipeListView):
    template_name = "recipes/pages/category.html"
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        qs = qs.filter(category__id=category_id, is_published=True).order_by('-created_at')
        return qs
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        category = Recipe.objects.filter(category__id=category_id).first().category
        context.update({
            'category': category,
            'title': f'{category.name}'
        })
        return context
    
class RecipeListViewSearch(RecipeListView):
    template_name = "recipes/pages/search.html"
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        qs = qs.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term),
            is_published=True
        ).order_by('-created_at')
        return qs
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        context.update({
            'search_term': search_term,
            'page_title': f'Search for "{search_term}"',
            'additional_url_query': f'&q={search_term}',
        })
        return context
