from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.front_page, name="front_page"),
    # path('signup/', views.signup, name='signup'),
    # path('login/', views.log_in, name='login'),
    # path('logout/', views.log_out, name='logout'),
    path('landingPage/', views.landingPage,name='landingPage'),
    path('register/', views.UserRegistrationRequest, name='register'),
    path('login/', views.UserLoginRequest, name='login'),
    path('logout', views.UserLogoutRequest, name='logout')
]
