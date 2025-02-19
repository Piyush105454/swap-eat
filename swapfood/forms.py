from django import forms
from .models import FoodPost

class FoodPostForm(forms.ModelForm):
    class Meta:
        model = FoodPost
        fields = ['photo', 'latitude', 'longitude']
