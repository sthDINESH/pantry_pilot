from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ShoppingList


@login_required
def shopping_list(request):
    """
    Display shopping list page with basic message
    
    **Template:**
    :template:`shopping/shopping_list.html`
    """
    shopping_lists = ShoppingList.objects.filter(
        user=request.user
    )
    context = {
        'page_title': 'Shopping Lists',
        'message': 'Welcome to your shopping lists! Feature coming soon...',
        'shopping_lists': shopping_lists,
    }
    return render(request, 'shopping/shopping_list.html', context)
