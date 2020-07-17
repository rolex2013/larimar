
from django.urls import path
#from .models import MainManu
#from .views import ProjectsHome
#from accounts.views import ELogoutView
from .views import notificationread, notificationfilter
from companies.views import contents, publiccontents, vacancies, vacancy_detail #, ContentList
from . import views

app_name = 'my_main'

urlpatterns = [
   #path('home/', views.ProjectsHome, name = 'home'),
   path('site/vacancies_page/', vacancies, name = 'vacancies'),
   path('site/vacancies_list/<int:pk>', vacancy_detail, name = 'vacancy_detail'),    
   path('', publiccontents, name = 'index'),
   path('main/', contents, name = 'main'),
   path('main/notify/', notificationread, name = 'notification_read'),
   path('main/notify_filter/', notificationfilter, name = 'notification_filter'),
   #path('', contents, name = 'main'),
   #path('', contents, name = 'index'),
   #path('', ELogoutView.as_view(), name='logout')
]