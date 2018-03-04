from django import forms

from .models import CheckOut


class CheckoutRequestForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ['check_in']
        widgets = {'check_in': forms.HiddenInput()}