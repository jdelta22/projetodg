from django import forms
from recipes.models import Recipe
from utils.recipes.djangoforms import add_placeholder, add_attr
from collections import defaultdict


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
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_steps = cleaned_data.get('preparation_steps')

        if len(title) < 6:
            self._my_errors['title'].append('The title must have at least 6 characters.')
        if len(description) < 10:
            self._my_errors['description'].append('The description must have at least 10 characters.')
        if len(preparation_steps) < 30:
            self._my_errors['preparation_steps'].append('The preparation steps must have at least 30 characters.')

        if self._my_errors:
            raise forms.ValidationError(self._my_errors)
        

        return super_clear
    
    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if preparation_time <= 0:
            raise forms.ValidationError('The preparation time must be greater than zero.')
        
        return preparation_time
    
    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if servings <= 0:
            raise forms.ValidationError('The servings must be greater than zero.')

        return servings
