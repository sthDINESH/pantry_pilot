from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def shopping_list(request):
    """
    Display shopping list page with basic message
    
    **Template:**
    :template:`shopping/shopping_list.html`
    """
    context = {
        'page_title': 'Shopping Lists',
        'message': 'Welcome to your shopping lists! Feature coming soon...'
    }
    return render(request, 'shopping/shopping_list.html', context)
