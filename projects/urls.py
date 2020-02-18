from django.urls import path
from .models import Project, Task, TaskComment
from . import views

app_name = 'my_project'

urlpatterns = [
    path('', views.ProjectsHome.as_view(), name = 'home'),
    path('projects_list/', views.ProjectsList.as_view(), name = 'projects'),
    path('projects_list/<int:pk>', views.ProjectDetail.as_view(), name = 'project_detail'),
    path('projects_list/project_add/', views.project_add, name='project_add'),
    #path('projects_list/project_update/<int:pk>',views.project_edit, name='project_update'),
    path('projects_list/project_update/<int:pk>', views.ProjectUpdate.as_view(), name = 'project_update'),
    path('projects_list/project_delete/<int:pk>', views.project_delete, name='project_delete'),
    path('projects_list/tasks_list/<int:pk>', views.TaskDetail.as_view(), name = 'task_detail'),
    path('projects_list/tasks_list/task_add/<int:projectid>', views.task_add, name='task_add'),
    #path('projects_list/tasks_list/task_edit/<int:taskid>', views.task_edit, name='task_edit'),    
    #path('projects_list/tasks_list/task_delete/<int:taskid>', views.task_delete, name='task_delete'),        
    path('projects_list/tasks_list/taskcomments_list/<int:pk>', views.CommentDetail.as_view(), name = 'taskcomment_detail'),
    path('projects_list/tasks_list/taskcomments_list/taskcomment_add/<int:taskid>', views.taskcomment_add, name='taskcomment_add'),
    #path('projects_list/tasks_list/taskcomments_list/taskcomment_edit/<int:taskcommentid>', views.taskcomment_edit, name = 'taskcomment_edit'),
    #path('projects_list/tasks_list/taskcomments_list/taskcomment_delete/<int:taskcommentid>', views.taskcomment_delete, name='taskcomment_delete'),    
    
    #path('contact_form/', views.Contacts, name = 'contacts'),
]
