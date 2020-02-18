from django.urls import path
from .models import Company, Project, Task, TaskComment
from . import views

app_name = 'my_project'

urlpatterns = [
    path('', views.ProjectsHome.as_view(), name = 'home'),
    path('companies_list/', views.CompaniesList.as_view(), name = 'companies'),
    path('companies_page/<int:pk>', views.company_page, name = 'children'),
    #path('projects_list/<int:pk>', views.ProjectsList.as_view(), name = 'projects'),
    path('companies_list/<int:pk>', views.CompanyDetail.as_view(), name = 'projects'),
    path('projects_list/<int:pk>', views.ProjectDetail.as_view(), name = 'project_detail'),
    path('projects_list/project_create/', views.ProjectCreate.as_view(), name='project_create'),
    path('projects_list/project_update/<int:pk>', views.ProjectUpdate.as_view(), name = 'project_update'),
    #path('projects_list/project_delete/<int:pk>', views.ProjectDelete.as_view(), name = 'project_delete'),
    path('projects_list/tasks_list/<int:pk>', views.TaskDetail.as_view(), name = 'task_detail'),
    path('projects_list/tasks_list/task_create/<int:projectid>', views.TaskCreate.as_view(), name='task_create'),
    path('projects_list/tasks_list/task_update/<int:pk>', views.TaskUpdate.as_view(), name='task_update'),    
    #path('projects_list/tasks_list/task_delete/<int:pk>', views.TaskDelete.as_view(), name='task_delete'),        
    path('projects_list/tasks_list/taskcomments_list/<int:pk>', views.TaskCommentDetail.as_view(), name = 'taskcomment_detail'),
    path('projects_list/tasks_list/taskcomments_list/taskcomment_create/<int:taskid>', views.TaskCommentCreate.as_view(), name='taskcomment_create'),
    path('projects_list/tasks_list/taskcomments_list/taskcomment_update/<int:pk>', views.TaskCommentUpdate.as_view(), name = 'taskcomment_update'),
    #path('projects_list/tasks_list/taskcomments_list/taskcomment_delete/<int:pk>', views.TaskCommentDelete.as_view(), name='taskcomment_delete'),    
    
    #path('contact_form/', views.Contacts, name = 'contacts'),
]
