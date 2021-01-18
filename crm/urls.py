#from django.contrib.auth import views
from django.urls import path

from companies.models import Company
from crm.models import Client #, ClientTask, ClientTaskComment

#from companies.views import CompaniesList, companies, CompanyDetail, CompanyCreate, CompanyUpdate
from crm.views import clients, ClientCreate, ClientUpdate, clienttasks, clienttaskcomments, ClientTaskCreate, clienttaskfilter

from . import views

app_name = 'my_crm'

urlpatterns = [
    path('clients_page0/', views.clients, name = 'clients0'),   # для вызова страницы списка клиентов для текущей компании
    path('clients_page/<int:companyid>/<int:pk>', views.clients, name = 'clients'),
    ##path('projects_list/<int:pk>', views.ProjectDetail.as_view(), name = 'project_detail'),
    path('clients_list/client_create/<int:companyid>', views.ClientCreate.as_view(), name='client_create'),
    path('clients_list/client_update/<int:pk>', views.ClientUpdate.as_view(), name='client_update'),
    #path('projects_list/project_update/<int:pk>', views.ProjectUpdate.as_view(), name = 'project_update'),
    ##path('projects_list/project_delete/<int:pk>', views.ProjectDelete.as_view(), name = 'project_delete'),
    ##path('project_list/project_filter/<int:companyid>', views.projectfilter, name = 'project_filter'),
    #path('project_list/project_filter/', views.projectfilter, name = 'project_filter'),
    #path('projects_list/project_history/<int:pk>', views.projecthistory, name = 'project_history'),    
    path('clienttasks_page/<int:clientid>/<int:pk>', views.clienttasks, name = 'clienttasks'),
    ##path('tasks_list/<int:pk>', views.TaskDetail.as_view(), name = 'task_detail'),
    path('clienttasks_list/clienttask_create/<int:clientid>/<int:parentid>', views.ClientTaskCreate.as_view(), name = 'clienttask_create'),
    #path('tasks_list/task_update/<int:pk>', views.TaskUpdate.as_view(), name = 'task_update'),    
    ##path('projects_list/tasks_list/task_delete/<int:pk>', views.TaskDelete.as_view(), name='task_delete'),  
    path('clienttasks_list/clienttask_filter/', views.clienttaskfilter, name = 'clienttask_filter'),
    #path('tasks_list/task_history/<int:pk>', views.taskhistory, name = 'task_history'),
    path('clienttaskcomments_page/<int:taskid>', views.clienttaskcomments, name = 'clienttaskcomments'),          
    #path('taskcomments_list/<int:pk>', views.TaskCommentDetail.as_view(), name = 'taskcomment_detail'),
    #path('taskcomments_list/taskcomment_create/<int:taskid>', views.TaskCommentCreate.as_view(), name = 'taskcomment_create'),
    #path('taskcomments_list/taskcomment_update/<int:pk>', views.TaskCommentUpdate.as_view(), name = 'taskcomment_update'),
]
