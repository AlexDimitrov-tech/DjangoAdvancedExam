from django import forms

from .models import Game


class GameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'categories':
                field.widget.attrs.setdefault('class', 'form-select')
            else:
                field.widget.attrs.setdefault('class', 'form-control')

    class Meta:
        model = Game
        fields = ('title', 'description', 'min_players', 'max_players', 'categories')

    def clean(self):
        cleaned = super().clean()
        min_players = cleaned.get('min_players')
        max_players = cleaned.get('max_players')
        if min_players and max_players and min_players > max_players:
            raise forms.ValidationError('Min players cannot be greater than max players.')
        return cleaned
