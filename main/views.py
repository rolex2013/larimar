from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView

from django.contrib.auth.decorators import login_required

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
class ProjectsHome(TemplateView):
   template_name = 'main.html'

#class Home(ListView):