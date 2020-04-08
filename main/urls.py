
from django.urls import path
#from .models import MainManu
#from .views import ProjectsHome
from companies.views import contents #,ContentList
from . import views


app_name = 'my_main'

urlpatterns = [
   path('', views.ProjectsHome.as_view(), name = 'home'),
   #path('', ContentList.as_view(), name = 'home'),
   path('main/', contents, name = 'main'),
]