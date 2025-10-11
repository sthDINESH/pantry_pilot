from datetime import datetime, date
from django.views.generic import TemplateView
from pantry.models import PantryItem
from recipes.models import SavedRecipe
from meals.models import MealPlanItem
from shopping.models import ShoppingList


class DashboardView(TemplateView):
    """
    Renders the home page view
    related to :model:`auth/User`

    **Context**
        `pantry_items_count`: count of user instances related to
            :model:`PantryItem`
        `saved_search_count`: count of user instances related to
            :model:`SavedRecipe`
        `upcoming_meal_title`: title field value related to
            :model:`MealPLanItem`
        `this_weeks_shopping_list`: instance related to
            :model:`ShoppingList`

    **Template**
        :template:`dashboard/dashboard.html`
    """
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add authentication-specific context
        if self.request.user.is_authenticated:
            # Add user-specific data here later (pantry stats, etc.)
            context['pantry_items_count'] = PantryItem.objects.filter(
                user=self.request.user
            ).count()

            context['saved_search_count'] = SavedRecipe.objects.filter(
                user=self.request.user,
                is_external=True,
            ).count()

            upcoming_meal = MealPlanItem.objects.filter(
                user=self.request.user,
                start_time__gte=datetime.now()
            ).order_by('start_time').first()
            context['upcoming_meal'] = upcoming_meal

            next_shopping_list = ShoppingList.objects.filter(
                user=self.request.user,
                week_end_date__gte=date.today(),
            ).order_by('week_start_date').first()
            context['next_shopping_list'] = next_shopping_list
        else:
            pass

        return context
