from django.contrib import admin
from django.urls import path, include
from WellWatchin import views


urlpatterns = [
    path('',views.loginview,name='loginview'),
    path('Home',views.home,name='home'),
    path('SignUp',views.signup,name='signup'),
    path('AboutUs',views.aboutus,name='aboutus'),
    path('ContactUs',views.contactus,name='contactus'),
    path('Profile',views.profile,name='profile'),
    path('LoginView',views.loginview,name='loginview'),
    path('Logout',views.logoutuser,name='logout'),
    path('Info',views.info,name='info'),
    path('Exercise',views.exercise,name='exercise'),
    path('BP',views.bp,name='bp'),
    path("Water",views.water_tracker,name="water"),
    path("Weight",views.weight_tracker,name="weight"),
    path("Sleep",views.sleep_tracker,name="contact"),
    path("Tabs",views.tabs,name="tabs"),
    path("BMI",views.bmi,name="bmi"),
    path("Events",views.events,name="events"),


]