from django import forms
from .models import RecipeType, Recipe
from django.core.exceptions import ValidationError


def file_size(value): # add this to some file where you can import it from
    limit = 8 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 8 MiB.')


class RecipeTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False

    class Meta:
        model = RecipeType
        fields = ('name', 'description',)


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['picture'].required = False
        self.fields['description'].required = False
        self.fields['description'].widget.attrs.update({'rows': 3})
        self.fields['pdf'].validators = [file_size]

    class Meta:
        model = Recipe
        fields = ('name', 'type', 'picture', 'pdf', 'description',)


class DeleteRecipeTypeForm(forms.Form):
    confirm = forms.CharField(widget=forms.HiddenInput(), initial='yes')
