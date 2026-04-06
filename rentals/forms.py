from django import forms

from .models import RentalRequest


class RentalRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.setdefault('class', 'form-control')
        self.fields['message'].widget.attrs.setdefault('placeholder', 'Optional note to the owner...')

    class Meta:
        model = RentalRequest
        fields = ('message',)
        help_texts = {
            'message': 'Optional: mention dates, meetup area, or anything the owner should know.',
        }


class RentalDecisionForm(forms.ModelForm):
    decision = forms.ChoiceField(
        choices=(
            (RentalRequest.Status.APPROVED, 'Approve'),
            (RentalRequest.Status.DENIED, 'Deny'),
        ),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Decision',
    )

    class Meta:
        model = RentalRequest
        fields = ()

    def clean_decision(self):
        decision = self.cleaned_data['decision']
        if decision not in {RentalRequest.Status.APPROVED, RentalRequest.Status.DENIED}:
            raise forms.ValidationError('Pick either Approve or Deny.')
        return decision


class RentalCancelForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ('game', 'borrower', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
            field.required = False
            field.widget.attrs.setdefault('class', 'form-control')
