from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('',views.sign, name="sign"),
   path('sign2',views.sign2, name="sign2"),
   path('home',views.home, name="home"),
   path('logout',views.logout, name="logout"),
   path('signup',views.signup, name="signup"),
   path('postsignup',views.postsignup, name="postsignup"),
   path('cancelsignup',views.cancelsignup, name="cancelsignup"),
   path('go',views.go, name="go")

]
