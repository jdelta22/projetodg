from django.shortcuts import render, redirect, reverse
from django.http import Http404 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as message
from .forms import RegisterForm, LoginForm, RecipeEditForm
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        message.success(request, 'Your user is created, please log in.')

        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')

def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username = form.cleaned_data.get('username', ''),
            password = form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            message.success(request, 'Login realizado com sucesso.')
            login(request, authenticated_user)
        else:
            message.error(request, 'Usuário ou senha inválidos.')
    else:   
        message.error(request, 'Erro ao validar formulário.')

    return redirect(reverse('authors:dashboard'))

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'
    )})

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, 'authors/pages/dashboard.html', {
        'user': request.user,
        'recipes': recipes
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()
    if not recipe:
        raise Http404()

    form = RecipeEditForm(
        data = request.POST or None,
        instance=recipe,
        files= request.FILES or None,
    )

    if form.is_valid():
        form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()

        message.success(request, 'Sua receita foi salva com sucesso.')
        message.info(request, 'Sua receita está em revisão e será publicada em breve.')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'authors/pages/dashboard-recipe.html', {
        'user': request.user,
        'recipe': recipe,
        'form': form,
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def recipe_create(request):
    form = RecipeEditForm(
        data = request.POST or None,
        files= request.FILES or None,
    )

    if form.is_valid():
        recipe: Recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()

        message.success(request, 'Sua receita foi salva com sucesso.')
        message.info(request, 'Sua receita está em revisão e será publicada em breve.')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))

    return render(request, 'authors/pages/recipecreate.html', {
        'user': request.user,
        'form': form,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')


    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()
    if not recipe:
        raise Http404()
    
    recipe.delete()
    message.success(request, 'Sua receita foi deletada com sucesso.')
    return redirect(reverse('authors:dashboard'))