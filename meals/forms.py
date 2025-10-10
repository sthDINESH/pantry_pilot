from django import forms
from .models import MealPlanItem, SavedRecipe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField


class MealPlanItemForm(forms.ModelForm):
    """
    Form for adding a single meal plan item
    related to :model:`MealPLanItem`
    """
    def __init__(self, *args, **kwargs):
        # Extract custom parameters
        user = kwargs.pop('user', None)
        selected_recipe_ids = kwargs.pop('selected_recipe_ids', None)

        super().__init__(*args, **kwargs)

        # Limit recipe choices to selected recipes only
        if user and selected_recipe_ids:
            self.fields['recipe'].queryset = SavedRecipe.objects.filter(
                id__in=selected_recipe_ids,
                user=user
            )
        elif user:
            # Fallback to user's saved recipes if no selection
            self.fields['recipe'].queryset = SavedRecipe.objects.filter(
                user=user
            )

        # Add Bootstrap classes to widgets WITHOUT placeholder
        # fix the issue with FloatingField in crispy forms adding
        # placeholder attribute for select element
        self.fields['recipe'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['meal_type'].widget.attrs.update({
            'class': 'form-select'
        })

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML('''
                <div class="form-floating mb-3">
                    <select name="recipe" class="form-select"
                            id="id_recipe" required>
                        {% for value, label in form.recipe.field.choices %}
                            <option value="{{ value }}"
                                    {% if value == form.recipe.value %}
                                    selected{% endif %}>
                                {{ label }}
                            </option>
                        {% endfor %}
                    </select>
                    <label for="id_recipe">Recipe*</label>
                </div>
            '''),
            Row(
                Column(
                    HTML('''
                    <div class="form-floating mb-3">
                        <select name="meal_type" class="form-select"
                                id="id_meal_type">
                        {% for value, label in form.meal_type.field.choices %}
                            <option value="{{ value }}"
                                {% if value == form.meal_type.value %}
                                selected
                                {% endif %}>
                                {{ label }}
                            </option>
                        {% endfor %}
                        </select>
                        <label for="id_meal_type">Meal Type</label>
                    </div>
                    '''),
                    css_class="col-8"
                ),
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
