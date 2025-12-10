from django import forms
from recipes.models import Recipe
from utils.recipes.djangoforms import add_placeholder, add_attr
from collections import defaultdict
from authors.validators import AuthorRecipeValidator


class RecipeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps', 'cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit',
                   'preparation_steps', 'cover',]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description'}),
            'category': forms.Select(),
            'preparation_time': forms.NumberInput(attrs={'placeholder': 'Preparation Time (minutes)'}),
            'preparation_time_unit':  forms.Select(choices=(("Minutes", "Minutes"), ("Hours", "Hours"))),
            'servings': forms.NumberInput(attrs={'placeholder': 'Servings'}),
            'servings_unit': forms.Select(choices=(("Portions", "Portions"), ("People", "People"), ("Units", "Units"),
                                                    ("Pieces", "Pieces"), ("Units", "Units"))),
            
            'preparation_steps': forms.Textarea(attrs={'placeholder': 'Preparation Steps'}),
            'cover': forms.FileInput(attrs={'class': 'span-2'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Tags (separated by commas)'}),
        }

    def clean(self, *args, **kwargs ):
        super_clear = super().clean(*args, **kwargs)
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clear
    
   