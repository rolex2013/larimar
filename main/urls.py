
from django.urls import path
#from .models import MainManu
from .views import ProjectsHome
from . import views


app_name = 'my_main'

urlpatterns = [
   path('', views.ProjectsHome.as_view(), name = 'home'),
]