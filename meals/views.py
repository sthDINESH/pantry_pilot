from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def meals_list(request):
    """
    Display meals planning page
    """
    context = {
        'page_title': 'Meal Planning',
    }
    return render(request, 'meals/meals_list.html', context)
