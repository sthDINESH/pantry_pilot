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


class ResolveDuplicateItemForm(forms.Form):
    """
    Form for handling duplicate pantry item resolution
    """
    ACTION_CHOICES = [
        ('add_quantity', 'Add to Existing'),
        ('replace_quantity', 'Replace Existing'),
    ]
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.HiddenInput()
    )
    quantity = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.HiddenInput()
    )
    units = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.HiddenInput()
    )
    category = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')

        if action == 'add_quantity':
            if not cleaned_data.get('quantity'):
                raise forms.ValidationError("Additional quantity is required for add action")
        elif action == 'replace_quantity':
            if not cleaned_data.get('quantity'):
                raise forms.ValidationError("New quantity is required for replace action")
            if not cleaned_data.get('units'):
                raise forms.ValidationError("Units are required for replace action")
            if not cleaned_data.get('category'):
                raise forms.ValidationError("Category required for replace action")
        return cleaned_data
