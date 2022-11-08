from django import forms
from django.core.exceptions import ValidationError

from .models import PrecautionType, Precaution


def docs_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 8 MiB.')


class PrecautionTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = PrecautionType
        fields = ('name', 'description')


class PrecautionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['cover'].required = False
        self.fields['description'].widget.attrs.update({'rows': 3})
        self.fields['file'].validators = [docs_size]

    class Meta:
        model = Precaution
        fields = ('name', 'precaution_type', 'cover', 'description', 'file',)