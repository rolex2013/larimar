from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeProjectsView.as_view(), name = 'home'),
    path('projects/', views.ListProjectsView.as_view(), name = 'projects'),
]
