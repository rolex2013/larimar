
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
    path('docs_list/doc_docver/', views.docver_change, name='docver_change'),
    path('doctasks_page/<int:pk>', views.doctasks, name='doctasks'),
    #path('doctasks_page/<int:pk>', views.doctasks, name='doctasks'),
    path('doctasks_list/doctask_create/<int:docid>/<int:docverid>', views.DocTaskCreate.as_view(), name='doctask_create'),
    #path('doctasks_list/doctask_create/<int:docid>', views.DocTaskCreate.as_view(), name='doctask_create'),
    path('doctasks_list/doctask_update/<int:pk>', views.DocTaskUpdate.as_view(), name='doctask_update'),
    #path('doctaskcomments_page/<int:taskid>', views.doctaskcomments, name='doctaskcomments'),
    #path('doctaskcomments_list/doctaskcomment_create/<int:taskid>', views.DocTaskCommentCreate.as_view(),
    #     name='doctaskcomment_create'),
    ##path('doctaskcomments_list/doctaskcomment_update/<int:pk>', views.DocTaskCommentUpdate.as_view(),
    ##     name='doctaskcomment_update'),
]
