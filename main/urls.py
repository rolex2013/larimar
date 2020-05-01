
from django.urls import path
#from .models import MainManu
#from .views import ProjectsHome
#from accounts.views import ELogoutView
from companies.views import contents, publiccontents #, ContentList
from . import views

app_name = 'my_main'

urlpatterns = [
   #path('home/', views.ProjectsHome, name = 'home'),
   path('', publiccontents, name = 'index'),
   path('main/', contents, name = 'main'),
   #path('', contents, name = 'main'),
   #path('', contents, name = 'index'),
   #path('', ELogoutView.as_view(), name='logout')
]