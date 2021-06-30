
from django.urls import path

#from companies.models import Company
#from files.models import Project, Task, TaskComment

#from companies.views import CompaniesList, companies, CompanyDetail, CompanyCreate, CompanyUpdate
from . import views

app_name = 'my_file'

urlpatterns = [
    #path('docs/docs', views.docs, name='doc_docs'),  # для вызова главной страницы приложения Файлы
    path('files_page0/', views.folders, name='folders0'),  # для вызова страницы списка файлов для текущей компании
    path('files_page/<int:companyid>/<int:pk>', views.folders, name='folders'),
    path('files_list/folder_create/<int:companyid>/<int:parentid>', views.FolderCreate.as_view(), name='folder_create'),
    path('files_list/folder_update/<int:pk>', views.FolderUpdate.as_view(), name='folder_update'),

    #path('files_page/<int:pk>', views.doctasks, name='doctasks'),
    #path('filetasks_list/doctask_create/<int:docid>/<int:docverid>', views.DocTaskCreate.as_view(), name='file_create'),
    #path('filefiles_list/doctask_update/<int:pk>', views.DocTaskUpdate.as_view(), name='file_update'),
]
