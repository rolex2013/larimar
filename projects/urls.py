#from django.contrib.auth import views
from django.urls import path
from .models import Company, Project, Task, TaskComment
from . import views

app_name = 'my_project'

urlpatterns = [
    #path('login/', views.LoginView.as_view(), name='login'),
    path('', views.ProjectsHome.as_view(), name = 'home'),
    path('menu_companies/', views.CompaniesList.as_view(), name = 'menu_companies'),
    path('companies_page/<int:pk>', views.companies, name = 'companies'),
    #path('projects_list/<int:pk>', views.ProjectsList.as_view(), name = 'projects'),
    path('companies_list/<int:pk>', views.CompanyDetail.as_view(), name = 'company_detail'),
    path('companies_list/company_create/<int:parentid>', views.CompanyCreate.as_view(), name = 'company_create'),
    path('companies_list/company_update/<int:pk>', views.CompanyUpdate.as_view(), name = 'company_update'),
    path('projects_page/<int:companyid>/<int:pk>', views.projects, name = 'projects'),
    #path('projects_list/<int:pk>', views.ProjectDetail.as_view(), name = 'project_detail'),
    path('projects_list/project_create/<int:companyid>/<int:parentid>', views.ProjectCreate.as_view(), name='project_create'),
    path('projects_list/project_update/<int:pk>', views.ProjectUpdate.as_view(), name = 'project_update'),
    #path('projects_list/project_delete/<int:pk>', views.ProjectDelete.as_view(), name = 'project_delete'),
    path('tasks_page/<int:projectid>/<int:pk>', views.tasks, name = 'tasks'),
    path('tasks_list/<int:pk>', views.TaskDetail.as_view(), name = 'task_detail'),
    path('tasks_list/task_create/<int:projectid>/<int:parentid>', views.TaskCreate.as_view(), name='task_create'),
    path('tasks_list/task_update/<int:pk>', views.TaskUpdate.as_view(), name='task_update'),    
    #path('projects_list/tasks_list/task_delete/<int:pk>', views.TaskDelete.as_view(), name='task_delete'),        
    path('taskcomments_list/<int:pk>', views.TaskCommentDetail.as_view(), name = 'taskcomment_detail'),
    path('taskcomments_list/taskcomment_create/<int:taskid>', views.TaskCommentCreate.as_view(), name='taskcomment_create'),
    path('taskcomments_list/taskcomment_update/<int:pk>', views.TaskCommentUpdate.as_view(), name = 'taskcomment_update'),
    #path('projects_list/tasks_list/taskcomments_list/taskcomment_delete/<int:pk>', views.TaskCommentDelete.as_view(), name='taskcomment_delete'),    
    
    #path('contact_form/', views.Contacts, name = 'contacts'),
]
