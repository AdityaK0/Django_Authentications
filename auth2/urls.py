
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home_page),
    path('login/',user_login),
    path('register/',register_login),
    path('logout/',logout),
    path('welcome/',protected_api)
    # path('auth/',include('auth2.urls')),
    
]
