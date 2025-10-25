from ..models import Recipe
from django.views.generic import DetailView

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/pages/recipe-view.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'is_detail_page': True,
        })
        return context