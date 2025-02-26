from django import forms
from .models import FoodPost
from .models import Invitation
class FoodPostForm(forms.ModelForm):
    class Meta:
        model = FoodPost
        fields = ['name', 'description','radius','photo','location']
# Invitation form
class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']

# Search form
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)
