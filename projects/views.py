from django.views.generic import TemplateView

class HomeProjectsView(TemplateView):
    template_name = 'home.html'

class ListProjectsView(TemplateView):
    template_name = 'projects.html'    
