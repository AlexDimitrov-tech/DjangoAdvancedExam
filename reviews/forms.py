from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

        self.fields['rating'].widget.attrs.setdefault('min', 1)
        self.fields['rating'].widget.attrs.setdefault('max', 5)
        self.fields['comment'].widget.attrs.setdefault('placeholder', 'Share what you liked (or didn\'t).')

    class Meta:
        model = Review
        fields = ('rating', 'comment')
        labels = {
            'rating': 'Rating (1 to 5)',
            'comment': 'Review',
        }
        help_texts = {
            'comment': 'Say what worked, what did not, and who the game is good for.',
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating


class ReviewDeleteForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
            field.required = False
            field.widget.attrs.setdefault('class', 'form-control')
