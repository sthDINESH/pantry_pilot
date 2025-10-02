from django import forms
from .models import MealPlanItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField


class MealPlanItemForm(forms.ModelForm):
    """
    Form for adding a single meal plan item
    related to :model:`MealPLanItem`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("recipe"),
            Row(
                Column(FloatingField("meal_type"), css_class="col-8"),
                Column(FloatingField("servings"), css_class="col-4"),
            ),
            Row(
                Column(
                    FloatingField("start_time"), 
                    css_class="col-6", 
                ),
                Column(
                    FloatingField("end_time"),
                    css_class="col-6",
                ),
            )
        )

    class Meta:
        model = MealPlanItem
        fields = (
            'recipe',
            'start_time',
            'end_time',
            'meal_type',
            'servings',
        )
