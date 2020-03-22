from django.contrib.auth import views
from django.urls import path
from django.conf.urls import url
 
from . import views

app_name = 'my_accounts'

urlpatterns = [
    path('login/', views.ELoginView.as_view(), name='login'),
    path('logout/', views.ELogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<int:userid>', views.UserProfileDetail.as_view(), name='profile'),
]