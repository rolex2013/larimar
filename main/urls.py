from django.urls import path

#from .models import MainManu
#from .views import ProjectsHome
#from accounts.views import ELogoutView
from .views import websocket_test, notificationread, notificationfilter, objecthistory, sidebarnotificationfilter, sidebarnotificationisread
from companies.views import contents, publiccontents, vacancies, vacancy_detail, SummaryCreate #, summaries, summary_detail #, ContentList
from . import views

app_name = 'my_main'

urlpatterns = [
   # path('home/', views.ProjectsHome, name = 'home'),
   path('site/vacancies_page/', vacancies, name='vacancies'),
   path('site/vacancies_list/<int:pk>', vacancy_detail, name='vacancy_detail'),
   # path('site/summary_page/<int:pk>/<int:site>', summaries, name = 'summaries_site'),
   # path('site/summaries_list/<int:pk>', summary_detail, name = 'summary_detail'), 
   path('site/summaries_list/<int:stafflistid>', SummaryCreate.as_view(), name='summary_create'),
   path('', publiccontents, name='index'),
   path('main/', contents, name='main'),
   path('main/notify/', notificationread, name='notification_read'),
   path('main/notify_filter/', notificationfilter, name='notification_filter'),
   path('main/object_history/<objtype>/<int:pk>', objecthistory, name='object_history'),
   path('main/objectfile_delete/<objtype>', views.objectfiledelete, name='objectfile_delete'),
   path('main/notifications/', views.notifications, name='notifications'),
   path('main/sidebar_notify_filter/', sidebarnotificationfilter, name='sidebar_notification_filter'),
   path('main/sidebar_notify_isread/', sidebarnotificationisread, name='sidebar_notification_isread'),
   path('main/ws/test/', websocket_test, name='websocket_test'),
   path('main/lang/', views.select_lang, name='select_lang'),
   # path('', contents, name = 'main'),
   # path('', contents, name = 'index'),
   # path('', ELogoutView.as_view(), name='logout')
]