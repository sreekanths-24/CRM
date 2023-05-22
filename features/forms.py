from django.contrib.auth.models import User
from django import forms
from .models import SupplierRecord

class AddSupplierRecord(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Name", "class":"form-control"}), label="")
    company_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Company Name", "class":"form-control"}), label="")
    Address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
    Product = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Product", "class":"form-control"}), label="")
    email =    forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone Number", "class":"form-control"}), label="")

    class Meta:
        model = SupplierRecord
        exclude = ("user",)