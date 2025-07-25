from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
      path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),  # Homepage with form & result
    # path('result/', views.result, name='result'),  # Remove this line
]
