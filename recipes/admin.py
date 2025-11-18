from django.contrib import admin
from .models import Category
from .models import Recipe
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...
class RecipeAdmin(admin.ModelAdmin):
    ...



@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display= ['id' ,'title','created_at', 'author', 'is_published' ]
    list_display_links = ['id', 'title', 'created_at']
    list_filter = ('is_published', 'created_at', 'category')
    search_fields = ('id', 'title','slug' , 'author__username', 'category__name', 'description')
    ordering = ('-created_at',)
    list_per_page = 15
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('tags',)

admin.site.register(Category, CategoryAdmin)