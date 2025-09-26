from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_bootstrap5.bootstrap5 import FloatingField

import config.constants as constants


class RecipeSearchForm(forms.Form):
    """
    Form for getting user preferences for recipe search
    """
    cuisine = forms.ChoiceField(
        choices=[('', 'Any Cuisine')] + constants.CUISINE_CHOICES,
        required=False,
        initial=''
    )

    diet = forms.ChoiceField(
        choices=[('', 'Any Diet')] + constants.DIET_CHOICES,
        required=False,
        initial=''
    )

    meal_type = forms.ChoiceField(
        choices=[('', 'Any Meal Type')] + constants.MEAL_TYPE_CHOICES,
        required=False,
        initial=''
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "recipe-search-form"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            FloatingField('cuisine'),
            FloatingField('diet'),
            FloatingField('meal_type'),
            Div(
                Submit(
                    'submit',
                    "Search",
                    css_class="btn btn-primary form-button"
                ),
                css_class="form-button-controls"
            )
        )
