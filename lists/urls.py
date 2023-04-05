from django.urls import path

from . import views

app_name = 'my_list'

urlpatterns = [
    path('lists_page0/', views.lists, name='lists0'),   # отображение списков для текущей компании
    path('lists_page/<int:companyid>/<int:pk>', views.lists, name='lists'),
    #path('lists_list/list_create/<int:companyid>/<int:parentid>', views.ListCreate.as_view(), name='list_create'),
    #path('lists_list/list_update/<int:pk>', views.ListUpdate.as_view(), name='list_update'),
    #дшыеpath('list_list/list_filter/', views.listfilter, name='list_filter'),

]
