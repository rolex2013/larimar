# from django.contrib.auth import views
from django.urls import path

# from companies.models import Company
# from projects.models import Project, Task, TaskComment

# from companies.views import CompaniesList, companies, CompanyDetail, CompanyCreate, CompanyUpdate
from . import views
# from main.views import objecthistory

app_name = 'my_project'

urlpatterns = [

    path('projects_page0/', views.projects, name='projects0'),   # для вызова страницы списка проектов для текущей компании
    path('projects_page/<int:companyid>/<int:pk>', views.projects, name='projects'),
    path('projects_list/project_create/<int:companyid>/<int:parentid>', views.ProjectCreate.as_view(), name='project_create'),
    path('projects_list/project_update/<int:pk>', views.ProjectUpdate.as_view(), name='project_update'),
    path('project_list/project_filter/', views.projectfilter, name='project_filter'),
    path('tasks_page/<int:projectid>/<int:pk>', views.tasks, name='tasks'),
    path('tasks_list/task_create/<int:projectid>/<int:parentid>', views.TaskCreate.as_view(), name='task_create'),
    path('tasks_list/task_update/<int:pk>', views.TaskUpdate.as_view(), name='task_update'),
    path('tasks_list/task_filter/', views.taskfilter, name='task_filter'),
    path('taskcomments_page/<int:taskid>', views.taskcomments, name='taskcomments'),
    path('taskcomments_list/<int:pk>', views.TaskCommentDetail.as_view(), name='taskcomment_detail'),
    path('taskcomments_list/taskcomment_create/<int:taskid>', views.TaskCommentCreate.as_view(), name='taskcomment_create'),
    path('taskcomments_list/taskcomment_update/<int:pk>', views.TaskCommentUpdate.as_view(), name='taskcomment_update'),
    path('projects_tasks/', views.projects_tasks, name='projects_tasks'),

]
