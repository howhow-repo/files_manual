from django import forms


class CheckLoginForm(forms.Form):
    confirm = forms.CharField(required=False)