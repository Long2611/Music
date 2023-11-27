from django import forms
from .models import SongRating

class SongRatingForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],  # Choices from 1 to 5
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SongRating
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class EditReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],  # Choices from 1 to 5
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = SongRating
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }