from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
import config.constants as constants


class RecipeSearchForm(forms.Form):
    """
    Form for getting user preferences for recipe search
    """
    cuisine = forms.ChoiceField(
        choices=[('', 'Any Cuisine')] + constants.CUISINE_CHOICES,
        required=False,
        initial='',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    diet = forms.ChoiceField(
        choices=[('', 'Any Diet')] + constants.DIET_CHOICES,
        required=False,
        initial='',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    meal_type = forms.ChoiceField(
        choices=[('', 'Any Meal Type')] + constants.MEAL_TYPE_CHOICES,
        required=False,
        initial='',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "recipe-search-form"
        self.helper.form_action = ""
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # Manual floating label structure for select fields
            # as FloatingField adds placeholder on select element
            Div(
                HTML('{{ form.cuisine }}'),  # Render just the widget
                HTML('<label for="id_cuisine">Cuisine</label>'),
                css_class="form-floating mb-3"
            ),
            Div(
                HTML('{{ form.diet }}'),  # Render just the widget
                HTML('<label for="id_diet">Diet</label>'),
                css_class="form-floating mb-3"
            ),
            Div(
                HTML('{{ form.meal_type }}'),  # Render just the widget
                HTML('<label for="id_meal_type">Meal type</label>'),
                css_class="form-floating mb-3"
            ),
        )
