
from django.urls import path

from companies.models import Company
from projects.models import Project, Task, TaskComment

#from companies.views import CompaniesList, companies, CompanyDetail, CompanyCreate, CompanyUpdate
from . import views

app_name = 'my_doc'

urlpatterns = [
    #path('docs/docs', views.docs, name='doc_docs'),  # для вызова главной страницы приложения Документы
    path('docs_page0/', views.docs, name='docs0'),  # для вызова страницы списка документов для текущей компании
    path('docs_page/<int:companyid>/<int:pk>', views.docs, name='docs'),
    path('docs_list/doc_create/<int:companyid>', views.DocCreate.as_view(), name='doc_create'),
    path('docs_list/doc_update/<int:pk>', views.DocUpdate.as_view(), name='doc_update'),
    path('docstasks_page/<int:docverid>/<int:pk>', views.doctasks, name = 'doctasks'),
    #path('doc/doc_list', views.doc_list, name='doc_list'),   # для вызова страницы списка Документов текущей Компании
    #path('doc/file_list', views.file_list, name='file_list'),   # для вызова страницы списка Файлов текущей Компании
]
