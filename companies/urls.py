from django.urls import path
# from django.conf.urls.static import static
# from django.conf import settings

# from .models import Company

# from .views import companies, CompanyDetail, CompanyCreate, CompanyUpdate #, CompaniesList
# from .views import ContentDetail, ContentCreate, ContentUpdate
# from .views import stafflist, StaffListCreate, StaffListUpdate, staffs, summaries, summary_detail, summary_delete #, summary_update,  #, StaffListDetail
# from .views import userroles, userrole_delete, userrole_create
# # from companies.views import CompaniesList, companies, CompanyDetail, CompanyCreate, CompanyUpdate
from . import views

app_name = 'my_company'

urlpatterns = [
    # path('menu_companies/', views.CompaniesList.as_view(), name='menu_companies'),
    path("companies_page/<int:pk>/<str:razdel>", views.companies, name="companies"),
    # path('projects_list/<int:pk>', views.ProjectsList.as_view(), name='projects'),
    path(
        "companies_list/company_detail/<int:pk>",
        views.CompanyDetail.as_view(),
        name="company-detail",
    ),
    path(
        "companies_list/company_create/<int:parentid>",
        views.CompanyCreate.as_view(),
        name="company_create",
    ),
    path(
        "companies_list/company_update/<int:pk>",
        views.CompanyUpdate.as_view(),
        name="company_update",
    ),
    path("stafflist_page/<int:companyid>/<int:pk>", views.stafflist, name="stafflist"),
    # path('stafflist_list/<int:pk>', views.StaffListDetail.as_view(), name='stafflist_detail'),
    path(
        "stafflist_list/stafflist_create/<int:companyid>/<int:parentid>",
        views.StaffListCreate.as_view(),
        name="stafflist_create",
    ),
    path(
        "stafflist_list/stafflist_update/<int:pk>",
        views.StaffListUpdate.as_view(),
        name="stafflist_update",
    ),
    path("staff_page/<int:stafflistid>/<int:pk>", views.staffs, name="staffs"),
    path(
        "staff_list/staff_create/<int:stafflistid>",
        views.StaffCreate.as_view(),
        name="staff_create",
    ),
    path(
        "staff_list/staff_update/<int:pk>",
        views.StaffUpdate.as_view(),
        name="staff_update",
    ),
    path("stafflist_detail/summaries_page/<int:pk>", views.summaries, name="summaries"),
    path(
        "stafflist_detail/summaries_list/summary_detail/<int:pk>",
        views.summary_detail,
        name="summary_detail",
    ),
    path(
        "stafflist_detail/summaries_list/summary_delete/<int:pk>",
        views.summary_delete,
        name="summary_delete",
    ),
    # path('content_page/<int:pk>', views.ContentList.as_view(), name='contents'),
    path(
        "content_list/content_detail/<int:pk>",
        views.ContentDetail.as_view(),
        name="content_detail",
    ),
    path(
        "content_list/content_create/",
        views.ContentCreate.as_view(),
        name="content_create",
    ),
    path(
        "content_list/content_update/<int:pk>",
        views.ContentUpdate.as_view(),
        name="content_update",
    ),
    path("user_detail/<int:companyid>/<int:pk>", views.userroles, name="user_detail"),
    path("user_detail/userroles/delete", views.userrole_delete, name="userrole_delete"),
    path("user_detail/userroles/create", views.userrole_create, name="userrole_create"),
]
