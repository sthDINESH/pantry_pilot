from django import forms
from .models import PantryItem, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField


class PantryItemForm(forms.ModelForm):
    """
    Form for adding single pantry item related to :model:`PantryItem`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("name"),
            Row(
                Column(FloatingField("quantity"), css_class="col-6"),
                Column(FloatingField("units"), css_class="col-6"),
            )
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.strip().title()
        return name

    class Meta:
        model = PantryItem
        fields = ('name', 'quantity', 'units')


class CategoryForm(forms.ModelForm):
    """
    Form for adding a category related to :model:`Category`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("category_name"),
        )

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
                raise forms.ValidationError(
                    "Additional quantity is required for add action"
                )
        elif action == 'replace_quantity':
            if not cleaned_data.get('quantity'):
                raise forms.ValidationError(
                    "New quantity is required for replace action"
                )
            if not cleaned_data.get('units'):
                raise forms.ValidationError(
                    "Units are required for replace action"
                )
            if not cleaned_data.get('category'):
                raise forms.ValidationError(
                    "Category required for replace action"
                )
        return cleaned_data
