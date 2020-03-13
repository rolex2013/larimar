from django.urls import path

from .models import Company
#from projects.models import Project, Task, TaskComment

from . import views

app_name = 'my_company'

urlpatterns = [    
    path('menu_companies/', views.CompaniesList.as_view(), name = 'menu_companies'),
    path('companies_page/<int:pk>', views.companies, name = 'companies'),
    #path('projects_list/<int:pk>', views.ProjectsList.as_view(), name = 'projects'),
    path('companies_list/<int:pk>', views.CompanyDetail.as_view(), name = 'company_detail'),
    path('companies_list/company_create/<int:parentid>', views.CompanyCreate.as_view(), name = 'company_create'),
    path('companies_list/company_update/<int:pk>', views.CompanyUpdate.as_view(), name = 'company_update'),
]