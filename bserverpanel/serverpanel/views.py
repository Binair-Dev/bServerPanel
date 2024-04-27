import threading
from django.shortcuts import redirect, render
from accounts.models import PanelUser
from serverpanel.models import Server
from .utils import downloader

def panel_server_list(request):
    try:
        paneluser = PanelUser.objects.get(user=request.user)
        servers = Server.objects.all().filter(owner=paneluser)
        return render(request, 'server-list.html', {'servers': servers, 'paneluser': paneluser})
    except PanelUser.DoesNotExist:
        return render(request, 'server-list.html', {})
    
def panel_server_one(request, id):
    try:
        server = Server.objects.get(id=id)
        return render(request, 'server-one.html', {'server': server})
    except Server.DoesNotExist:
        return render(request, 'server-one.html', {})
    
def panel_server_start(request, id):
    return redirect('server-one', id)

def panel_server_stop(request, id):
    return redirect('server-one', id)

def panel_server_restart(request, id):
    return redirect('server-one', id)

def panel_server_install(request, id):
    # Pour lancer le téléchargement dans un thread différent pour pas bloquer le site et rediriger vers la page du serveur
    # thread = threading.Thread(target=downloader.runDownload, args=(
    #     "https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/496/downloads/paper-1.20.4-496.jar", 
    #     'paper-1.20.4-496.jar', 
    #     'test')
    #     )
    # thread.start()
    
    # TODO: Remove
    downloader.runDownload(
        "https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/496/downloads/paper-1.20.4-496.jar", 
        'paper-1.20.4-496.jar', 
        'test')
    return redirect('server-one', id)