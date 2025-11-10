from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/<slug:slug>/', views.RecipeDetail.as_view(), name='recipe'),
    path('recipes/api/v1', views.RecipeListViewHomeApi.as_view(), name='recipes_api_v1'),
    path('recipes/api/v1/<int:pk>/', views.RecipeDetailApi.as_view(), name='recipe_api_v1_detail')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)