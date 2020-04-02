from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.db import transaction

from accounting.models import User, Seller, Company
from main.models import Product


class SellerCreateForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password("11111")
        user.is_seller = True
        user.save()
        seller = Seller.objects.create(user=user,address=self.cleaned_data["address"])
        return seller


class CompanyCreateForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password("11111")
        user.is_company = True
        user.save()
        company = Company.objects.create(user=user,name=self.cleaned_data["name"])
        return company


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'image','price','discounted_price','existStatus','brand','parent']