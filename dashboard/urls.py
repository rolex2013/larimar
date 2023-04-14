from django.urls import path
from . import views

app_name = 'my_dashboard'

urlpatterns = [
   path('dashboard_page0/', views.dashboard_lists, name='dashboard0'),
   path('dashboard_page/<int:companyid>', views.dashboard_lists, name='dashboard'),
]