from django import forms

from products.models import Category, Product, ProductMedia


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'quantity', 'description']


class ProductMediaForm(forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ['product', 'image']
