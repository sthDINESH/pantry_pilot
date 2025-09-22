from django import forms
from .models import PantryItem, Category


class PantryItemForm(forms.ModelForm):
    class Meta:
        model = PantryItem
        fields = ('name', 'quantity', 'units')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.strip().title()
        return name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)