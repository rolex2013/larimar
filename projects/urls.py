#from django.contrib.auth import views
from django.urls import path

from companies.models import Company
from projects.models import Project, Task, TaskComment

#from companies.views import CompaniesList, companies, CompanyDetail, CompanyCreate, CompanyUpdate
from . import views
#from main.views import objecthistory

app_name = 'my_project'

urlpatterns = [
    #path('login/', views.LoginView.as_view(), name='login'),
    #path('', views.ProjectsHome.as_view(), name = 'home'),
    path('projects_page0/', views.projects, name = 'projects0'),   # для вызова страницы списка проектов для текущей компании
    path('projects_page/<int:companyid>/<int:pk>', views.projects, name = 'projects'),
    #path('projects_list/<int:pk>', views.ProjectDetail.as_view(), name = 'project_detail'),
    path('projects_list/project_create/<int:companyid>/<int:parentid>', views.ProjectCreate.as_view(), name='project_create'),
    path('projects_list/project_update/<int:pk>', views.ProjectUpdate.as_view(), name = 'project_update'),
    #path('projects_list/project_delete/<int:pk>', views.ProjectDelete.as_view(), name = 'project_delete'),
    #path('project_list/project_filter/<int:companyid>', views.projectfilter, name = 'project_filter'),
    path('project_list/project_filter/', views.projectfilter, name = 'project_filter'),
    #path('projects_list/project_history/<int:pk>', views.projecthistory, name = 'project_history'),       
    path('tasks_page/<int:projectid>/<int:pk>', views.tasks, name = 'tasks'),
    #path('tasks_list/<int:pk>', views.TaskDetail.as_view(), name = 'task_detail'),
    path('tasks_list/task_create/<int:projectid>/<int:parentid>', views.TaskCreate.as_view(), name = 'task_create'),
    path('tasks_list/task_update/<int:pk>', views.TaskUpdate.as_view(), name = 'task_update'),    
    #path('projects_list/tasks_list/task_delete/<int:pk>', views.TaskDelete.as_view(), name='task_delete'),  
    path('tasks_list/task_filter/', views.taskfilter, name = 'task_filter'),
    #path('tasks_list/task_history/<int:pk>', views.taskhistory, name = 'task_history'),
    path('taskcomments_page/<int:taskid>', views.taskcomments, name = 'taskcomments'),          
    path('taskcomments_list/<int:pk>', views.TaskCommentDetail.as_view(), name = 'taskcomment_detail'),
    path('taskcomments_list/taskcomment_create/<int:taskid>', views.TaskCommentCreate.as_view(), name = 'taskcomment_create'),
    path('taskcomments_list/taskcomment_update/<int:pk>', views.TaskCommentUpdate.as_view(), name = 'taskcomment_update'),
    #path('projects_list/tasks_list/taskcomments_list/taskcomment_delete/<int:pk>', views.TaskCommentDelete.as_view(), name='taskcomment_delete'),    
    #path('contact_form/', views.Contacts, name = 'contacts'),
    path('tasks_page/projectfile_delete', views.projectfiledelete, name = 'projectfile_delete'),
]
