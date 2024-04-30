from django.urls import path
from . import views

urlpatterns = [
    path('servers/', views.panel_server_list, name='server-list'),
    path('server/<int:id>', views.panel_server_one, name='server-one'),
    path('server/start/<int:id>', views.panel_server_start, name='server-start'),
    path('server/stop/<int:id>', views.panel_server_stop, name='server-stop'),
    path('server/install/<int:id>', views.panel_server_install, name='server-install'),
    path('server/logs/<int:id>', views.panel_server_logs, name='server-logs'),
    path('server/create', views.panel_server_create, name='server-create'),
    path('server/delete/<int:id>', views.panel_server_delete, name='server-delete'),
    path('server/command/<int:id>/<str:cmd>/', views.panel_server_cmd, name='server-command'),
]
