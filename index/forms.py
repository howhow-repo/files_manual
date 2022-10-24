from django import forms
from phonenumber_field.formfields import PhoneNumberField
from employee.models import User


class UserProfileEdit(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].required = False

    class Meta:
        model = User
        fields = ['nickname', 'first_name', 'last_name', 'email', 'phone_number']
