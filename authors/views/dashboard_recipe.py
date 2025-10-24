from django.views import View 
from django.http.response import Http404
from django.shortcuts import render, redirect, reverse
from django.contrib import messages as message
from authors.forms import RecipeEditForm
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class dashboard_recipe(View):
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()
            
            if not recipe:
                raise Http404()
        return recipe

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard-recipe.html', {
        'form': form,
        })


    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = RecipeEditForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = RecipeEditForm(
            data=request.POST or None,
            instance=recipe,
            files=  request.FILES or None,
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()

            message.success(request, 'Your recipe is saved successfully!')
            message.info(request, 'Your recipe is under review and will be published soon.')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))

        return self.render_recipe(form)


@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch') 
class dashboard_recipe_delete(dashboard_recipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        message.success(self.request, 'Your recipe has been deleted successfully.')
        return redirect(reverse('authors:dashboard'))