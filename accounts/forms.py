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

        # plain placeholders are enough here, no need to get cute with them
        placeholders = {
            'username': 'Choose a username',
            'email': 'you@example.com',
            'first_name': 'First name',
            'last_name': 'Last name',
            'location': 'City or area',
            'avatar': 'https://example.com/avatar.jpg',
            'bio': 'Tell people a bit about your game taste',
        }
        for name, placeholder in placeholders.items():
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault('placeholder', placeholder)

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
        help_texts = {
            'location': 'Optional. Helpful when arranging local meetups.',
            'avatar': 'Optional public image URL.',
            'bio': 'Optional short profile summary.',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', '')
        # keeping this strict avoids weird half-valid values in the profile page
        if avatar and not avatar.startswith(('http://', 'https://')):
            raise forms.ValidationError('Avatar must be a valid URL (http/https).')
        return avatar


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'location',
            'avatar',
            'bio',
        )
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'location': 'Location',
            'avatar': 'Avatar URL',
            'bio': 'Short bio',
        }
        help_texts = {
            'location': 'Optional. A city or area is enough.',
            'avatar': 'Optional public image URL.',
            'bio': 'A short profile note for other users.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

        self.fields['first_name'].widget.attrs.setdefault('placeholder', 'First name')
        self.fields['last_name'].widget.attrs.setdefault('placeholder', 'Last name')
        self.fields['email'].widget.attrs.setdefault('placeholder', 'you@example.com')
        self.fields['location'].widget.attrs.setdefault('placeholder', 'City or area')
        self.fields['avatar'].widget.attrs.setdefault('placeholder', 'https://example.com/avatar.jpg')
        self.fields['bio'].widget.attrs.setdefault('placeholder', 'A few words about your game taste')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', '')
        if avatar and not avatar.startswith(('http://', 'https://')):
            raise forms.ValidationError('Avatar must be a valid URL (http/https).')
        return avatar
