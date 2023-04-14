#from django.contrib.auth import views
from django.urls import path

from companies.models import Company
from crm.models import Client #, ClientTask, ClientTaskComment, ClientEvent, ClientEventComment

from crm.views import clients, clienttasks, clienttaskcomments, clientevents, clienteventcomments
from crm.views import ClientCreate, ClientUpdate, ClientTaskCreate, ClientTaskUpdate, ClientTaskCommentCreate, ClientTaskCommentUpdate, ClientEventCreate, ClientEventUpdate, ClientEventCommentCreate, ClientEventCommentUpdate
from crm.views import clientfilter, clienttaskfilter, clienteventfilter
#from crm.views import clienthistory, clienttaskhistory, clienteventhistory

from . import views

app_name = 'my_crm'

urlpatterns = [
    path('clients_page0/', views.clients, name='clients0'),   # для вызова страницы списка клиентов для текущей компании
    path('clients_page/<int:companyid>/<int:pk>', views.clients, name='clients'),
    ##path('projects_list/<int:pk>', views.ProjectDetail.as_view(), name='project_detail'),
    path('clients_list/client_create/<int:companyid>', views.ClientCreate.as_view(), name='client_create'),
    path('clients_list/client_update/<int:pk>', views.ClientUpdate.as_view(), name='client_update'),
    #path('projects_list/project_update/<int:pk>', views.ProjectUpdate.as_view(), name='project_update'),
    ##path('projects_list/project_delete/<int:pk>', views.ProjectDelete.as_view(), name='project_delete'),
    ##path('project_list/project_filter/<int:companyid>', views.projectfilter, name='project_filter'),
    path('clients_list/client_filter/', views.clientfilter, name='client_filter'),
    #path('clients_list/client_history/<int:pk>', views.clienthistory, name='client_history'),    
    path('clienttasks_page/<int:clientid>/<int:pk>', views.clienttasks, name='clienttasks'),
    ##path('tasks_list/<int:pk>', views.TaskDetail.as_view(), name='task_detail'),
    path('clienttasks_list/clienttask_create/<int:clientid>/<int:parentid>', views.ClientTaskCreate.as_view(), name='clienttask_create'),
    path('clienttasks_list/clienttask_update/<int:pk>', views.ClientTaskUpdate.as_view(), name='clienttask_update'),    
    ##path('projects_list/tasks_list/task_delete/<int:pk>', views.TaskDelete.as_view(), name='task_delete'),  
    path('clienttasks_list/clienttask_filter/', views.clienttaskfilter, name='clienttask_filter'),
    #path('clienttasks_list/clienttask_history/<int:pk>', views.clienttaskhistory, name='clienttask_history'),
    path('clienttaskcomments_page/<int:taskid>', views.clienttaskcomments, name='clienttaskcomments'),          
    #path('taskcomments_list/<int:pk>', views.TaskCommentDetail.as_view(), name='taskcomment_detail'),
    path('clienttaskcomments_list/clienttaskcomment_create/<int:taskid>', views.ClientTaskCommentCreate.as_view(), name='clienttaskcomment_create'),
    path('clienttaskcomments_list/clienttaskcomment_update/<int:pk>', views.ClientTaskCommentUpdate.as_view(), name='clienttaskcomment_update'),
    path('clientevents_page/<int:clientid>/<int:pk>', views.clientevents, name='clientevents'),
    path('clientevents_list/clientevent_create/<int:clientid>/<int:taskid>', views.ClientEventCreate.as_view(), name='clientevent_create'),
    path('clientevents_list/clientevent_update/<int:pk>', views.ClientEventUpdate.as_view(), name='clientevent_update'),    
    path('clientevents_list/clientevent_filter/', views.clienteventfilter, name='clientevent_filter'),
    #path('clientevents_list/clientevent_history/<int:pk>', views.clienteventhistory, name='clientevent_history'),
    path('clienteventcomments_page/<int:eventid>', views.clienteventcomments, name='clienteventcomments'),
    path('clienteventcomments_list/clienteventcomment_create/<int:eventid>', views.ClientEventCommentCreate.as_view(), name='clienteventcomment_create'),
    path('clienteventcomments_list/clienteventcomment_update/<int:pk>', views.ClientEventCommentUpdate.as_view(), name='clienteventcomment_update'),        
]
