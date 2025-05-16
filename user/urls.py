from django.urls import path,include
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('login/',login_user,name='login'),
    path('register/',register,name='register'),
    path('logout/',logout_user,name='logout_user'),
    path('userlist/',userlist,name='userlist'),
    
]
