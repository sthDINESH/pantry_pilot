from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class DashboardView(TemplateView):
    """
    """
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # # context['page_title'] = 'Dashboard'
        
        # # Add authentication-specific context
        # if self.request.user.is_authenticated:
        #     # context['is_authenticated'] = True
        #     # Add user-specific data here later (pantry stats, etc.)
        # else:
        #     # context['is_authenticated'] = False
        #     # Add general information for anonymous users
            
        return context
