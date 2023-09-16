from django import forms
from .models import Vendors

class VendorForms(forms.ModelForm):
    class Meta:
        model = Vendors
        fields = ['vendor_name', 'vendor_license']
    
