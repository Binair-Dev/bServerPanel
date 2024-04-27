from django.urls import path
from . import views

urlpatterns = [
    path('servers/', views.panel_server_list, name='server-list'),
    path('server/<int:id>', views.panel_server_one, name='server-one'),
    path('server/start/<int:id>', views.panel_server_start, name='server-start'),
    path('server/stop/<int:id>', views.panel_server_stop, name='server-stop'),
    path('server/restart/<int:id>', views.panel_server_restart, name='server-restart'),
    path('server/install/<int:id>', views.panel_server_install, name='server-install'),
]
