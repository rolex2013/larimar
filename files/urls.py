
from django.urls import path

#from companies.models import Company
#from files.models import Project, Task, TaskComment

#from companies.views import CompaniesList, companies, CompanyDetail, CompanyCreate, CompanyUpdate
from . import views

app_name = 'my_file'

urlpatterns = [
    path('files_page0/', views.folders, name='folders0'),  # для вызова страницы списка файлов для текущей компании
    path('files_page/<int:companyid>/<int:pk>', views.folders, name='folders'),
    path('files_list/folder_create/<int:companyid>/<int:parentid>', views.FolderCreate.as_view(), name='folder_create'),
    path('files_list/folder_update/<int:pk>', views.FolderUpdate.as_view(), name='folder_update'),
    path('files_list/files_upload/<int:pk>', views.UploadFiles.as_view(), name='files_upload'),
    path('files_list/folder_filter/', views.folderfilter, name='folder_filter'),
    path('files_list/file_filter/', views.filefilter, name='file_filter'),
]
