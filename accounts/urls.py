from django.contrib.auth import views
from django.urls import path
from django.conf.urls import url
 
from . import views
from companies.views import publiccontents

from .decorators import check_recaptcha

app_name = 'my_account'

urlpatterns = [
    path('', views.ELogoutView.as_view(), name='logout0'),
    path('login/', views.ELoginView.as_view(), name='login'),
    #path('logout/', views.ELogoutView.as_view(), name='logout'),
    path('logout/', views.logout_view, name='logout'),
    #path('logout/', publiccontents, name = 'logout'),
    path('register/', check_recaptcha(views.register), name='register'),
    path('profile0/', views.UserProfileDetail, name='userprofile_detail0'),
    path('profile/<int:userid>/<param>', views.UserProfileDetail, name='userprofile_detail'),
    path('profile/update/<int:pk>', views.UserProfileUpdate.as_view(), name='userprofile_update'),
]