from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.panel_user_list, name='user-list'),
    path('login/', views.panel_user_login, name='user-login'),
    path('register/', views.panel_user_register, name='user-register'),
    path('logout/', views.panel_user_logout, name='user-logout'),
    path('profile/', views.panel_user_profile, name='user-profile'),
]
