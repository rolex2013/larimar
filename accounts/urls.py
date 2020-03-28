from django.contrib.auth import views
from django.urls import path
from django.conf.urls import url
 
from . import views

app_name = 'my_account'

urlpatterns = [
    path('login/', views.ELoginView.as_view(), name='login'),
    path('logout/', views.ELogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    #path('profile/<int:userid>', views.UserProfileDetail.as_view(), name='profile'),
    path('profile0/', views.UserProfileDetail, name='userprofile_detail0'),
    path('profile/<int:userid>', views.UserProfileDetail, name='userprofile_detail'),
    path('profile/update/<int:pk>', views.UserProfileUpdate.as_view(), name='userprofile_update'),
]