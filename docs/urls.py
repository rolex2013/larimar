
from django.urls import path

from companies.models import Company
from projects.models import Project, Task, TaskComment

#from companies.views import CompaniesList, companies, CompanyDetail, CompanyCreate, CompanyUpdate
from . import views

app_name = 'my_doc'

urlpatterns = [
    #path('doc/doc_list', views.docs, name='doc_list'),   # для вызова страницы списка Документов текущей Компании
    #path('doc/file_list', views.files, name='file_list'),   # для вызова страницы списка Файлов текущей Компании
]
