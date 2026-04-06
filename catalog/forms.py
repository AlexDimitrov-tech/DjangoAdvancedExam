from django import forms

from .models import Category, Game


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        labels = {'name': 'Category name'}
        help_texts = {'name': 'Use short, clear labels such as Strategy, Party, or Family.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.setdefault('class', 'form-control')
        self.fields['name'].widget.attrs.setdefault('placeholder', 'Example: Strategy')


class CategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'created_by')
        labels = {'created_by': 'Created by'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
            field.required = False
            field.widget.attrs.setdefault('class', 'form-control')


class GameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'categories':
                field.widget.attrs.setdefault('class', 'form-select')
                field.help_text = 'Hold Ctrl/Cmd if you want to pick more than one.'
            else:
                field.widget.attrs.setdefault('class', 'form-control')

        self.fields['title'].widget.attrs.setdefault('placeholder', 'Example: Catan')
        self.fields['description'].widget.attrs.setdefault(
            'placeholder',
            'Short note about the game, vibe, or why it is fun for your group.',
        )

    class Meta:
        model = Game
        fields = ('title', 'description', 'cover_image', 'min_players', 'max_players', 'categories')
        labels = {
            'cover_image': 'Cover image',
            'min_players': 'Minimum players',
            'max_players': 'Maximum players',
        }
        help_texts = {
            'cover_image': 'Upload a clear cover photo or promotional image.',
            'min_players': 'Smallest group size this game supports.',
            'max_players': 'Largest group size this game supports.',
        }

    def clean(self):
        cleaned = super().clean()
        min_players = cleaned.get('min_players')
        max_players = cleaned.get('max_players')
        if min_players and max_players and min_players > max_players:
            raise forms.ValidationError('Min players cannot be greater than max players.')
        return cleaned


class GameDeleteForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'owner')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
            field.required = False
            field.widget.attrs.setdefault('class', 'form-control')
