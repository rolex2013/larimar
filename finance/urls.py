from django.urls import path
from . import views

app_name = 'my_finance'

urlpatterns = [
   path('', views.finance, name = 'finance'),
   path('curr_rate_filter/', views.currencyratefilter, name = 'currency_rate_filter'),
]