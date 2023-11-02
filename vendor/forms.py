from django import forms
from .models import Vendors
from accounts.validators import allow_only_images_validator

class VendorForms(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}),validators=[allow_only_images_validator])
    class Meta:
        model = Vendors
        fields = ['vendor_name', 'vendor_license']
    
