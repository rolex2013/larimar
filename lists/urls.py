from django.urls import path

from . import views

app_name = 'my_list'

urlpatterns = [

    path('lists_page0/', views.ylists, name='ylists0'),   # отображение списков для текущей компании
    path('lists_page/<int:companyid>/<int:pk>', views.ylists, name='ylists'),
    path('lists_list/list_create/<int:companyid>', views.YListCreate.as_view(), name='ylist_create'),
    path('lists_list/list_view/<int:pk>', views.ylist_items, name='ylist_items'),
    path('lists_list/list_update/<int:pk>', views.YListUpdate.as_view(), name='ylist_update'),
    path('list_list/list_filter/', views.ylistfilter, name='ylist_filter'),
    # path('list_page/item_edit/<int:prz>/<int:pk>/<int:sort>', views.yitemedit, name='yitem_edit'),
    path('list_page/item_edit/', views.yitemedit, name='yitem_edit'),

]
