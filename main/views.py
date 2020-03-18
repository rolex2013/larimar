from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView


class ProjectsHome(TemplateView):
   template_name = 'home.html'