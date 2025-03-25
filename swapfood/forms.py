from django import forms
from .models import FoodPost
from .models import Invitation
from .models import FoodImage

class FoodImageForm(forms.ModelForm):
    class Meta:
        model = FoodImage
        fields = ['image']
class FoodPostForm(forms.ModelForm):
    class Meta:
        model = FoodPost
        fields = ['name', 'description','radius','photo','location']
        labels = {'location': 'Pincode'}
# Invitation form
class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']

# Search form
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)
