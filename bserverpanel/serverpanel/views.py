import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from accounts.models import PanelUser
from serverpanel.utils.command_type import CommandType
from serverpanel.models import Server
from .utils import downloader
from .utils import files
from .utils import unzipper
from .utils import user_utils
from .utils.sub_server import SubServer

running_servers = {}

def panel_server_list(request):
    try:
        paneluser = PanelUser.objects.get(user=request.user)
        servers = Server.objects.all().filter(owner=paneluser)
        return render(request, 'server-list.html', {'servers': servers, 'paneluser': paneluser})
    except PanelUser.DoesNotExist:
        return render(request, 'server-list.html', {})
    
def panel_server_one(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        try:
            server = Server.objects.get(id=id)
            try:
                logs_file = files.get_latest_log_file(os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, server.directory))
                if logs_file is None:
                    return render(request, 'server-one.html', {'server': server, 'logs': 'Aucun fichier logs trouvé !'})
                else:
                    token = files.get_logs_with_token(os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, server.directory))
                    with open(logs_file, 'r') as fichier:
                        logs = fichier.read()
                        return render(request, 'server-one.html', {'server': server, 'logs': logs, 'token': token})
            except FileNotFoundError:
                return render(request, 'server-one.html', {'server': server, 'logs': 'Aucun fichier logs trouvé !'})
        except Server.DoesNotExist:
            return render(request, 'server-one.html', {})
    else:
        return render(request, 'server-not-accessible.html')
    
def panel_server_start(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        if f"{id}" in running_servers:
            response = HttpResponse(f'<script>alert("Le serveur est déjà démarré."); window.location.href="/panel/server/{id}";</script>')
            return response
        else:
            server = Server.objects.get(id=id)
            sub_server = SubServer(
                os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, server.directory), 
                server.max_ram, 
                server.start_command, 
                server.stop_command,
                server.game)
            done = sub_server.start_server()
            running_servers[f"{id}"] = sub_server
            if done:
                response = HttpResponse(f'<script>alert("Le serveur a bien été démarré."); window.location.href="/panel/server/{id}";</script>')
            else:
                response = HttpResponse(f'<script>alert("Le serveur n\'a pas pu être demarré."); window.location.href="/panel/server/{id}";</script>')
            return response
    else:
        return render(request, 'server-not-accessible.html')

def panel_server_stop(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        db_server = server = Server.objects.get(id=id)
        if f"{id}" in running_servers:
            server = running_servers[f"{id}"]
            done = server.stop_server()
            if done:
                del running_servers[f"{id}"]
                response = HttpResponse(f'<script>alert("Le serveur a bien été arrêté."); window.location.href="/panel/server/{id}";</script>')
            else:
                response = HttpResponse(f'<script>alert("Le serveur n\'a pas pu être arrêté."); window.location.href="/panel/server/{id}";</script>')
            return response
        response = HttpResponse(f'<script>alert("Le serveur n\'est pas demarré."); window.location.href="/panel/server/{id}";</script>')
        return response
    else:
        return render(request, 'server-not-accessible.html')

def panel_server_restart(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        if f"{id}" in running_servers:
            server = running_servers[f"{id}"]
            done = server.restart_server()
            if done:
                response = HttpResponse(f'<script>alert("Le serveur a bien été redémarré."); window.location.href="/panel/server/{id}";</script>')
            else:
                response = HttpResponse(f'<script>alert("Le serveur n\'a pas pu être redémarré."); window.location.href="/panel/server/{id}";</script>')
            return response
        response = HttpResponse(f'<script>alert("Le serveur n\'est pas demarré."); window.location.href="/panel/server/{id}";</script>')
        return response
    else:
        return render(request, 'server-not-accessible.html')

def panel_server_cmd(request, id):
    pass

def panel_server_install(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        server = Server.objects.get(id=id)
        configuration = server.configuration

        for command in configuration.commands.all().order_by('position'):
            if command.command_type == CommandType.LINK.value:
                downloader.runDownload(command.link, command.file_name, server.directory)
            elif command.command_type == CommandType.ACCEPT_EULA.value:
                files.create_eula_file(server.directory)
            elif command.command_type == CommandType.UNZIP.value:
                unzipper.decompress_archive(f"{settings.DEFAULT_INSTALLATION_DIRECTORY}/{server.directory}/{command.file_name}", f"{settings.DEFAULT_INSTALLATION_DIRECTORY}/{server.directory}")
            elif command.command_type == CommandType.COMMAND_LINE.value:
                pass

        response = HttpResponse(f'<script>alert("L\'installation a bien été éxécutée."); window.location.href="/panel/server/{id}";</script>')
        return response
    else:
        return render(request, 'server-not-accessible.html')

def panel_server_logs(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        try:
            server = Server.objects.get(id=id)
            try:
                logs_file = files.get_latest_log_file(os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, server.directory))
                if logs_file is None:
                    return HttpResponse("Aucun fichier logs trouvé !")
                else:
                    with open(logs_file, 'r') as fichier:
                        logs = fichier.read()
                        return HttpResponse(logs)
            except FileNotFoundError:
                return HttpResponse("Aucun fichier logs trouvé !")
        except Server.DoesNotExist:
            return HttpResponse("Aucun fichier logs trouvé !")
    else:
        return render(request, 'server-not-accessible.html')