from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = 'form-control'
            if getattr(field.widget, 'input_type', None) == 'checkbox':
                css_class = 'form-check-input'
            field.widget.attrs.setdefault('class', css_class)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'location',
            'avatar',
            'bio',
        )

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', '')
        if avatar and not avatar.startswith(('http://', 'https://')):
            raise forms.ValidationError('Avatar must be a valid URL (http/https).')
        return avatar


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
