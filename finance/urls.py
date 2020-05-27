from django.urls import path
from . import views

app_name = 'my_finance'

urlpatterns = [
   path('', views.finance, name = 'finance'),
]