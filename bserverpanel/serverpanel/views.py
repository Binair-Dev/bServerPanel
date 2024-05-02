import os
import random
import shutil
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import PanelUser
from serverpanel.forms import CreateServerForm
from serverpanel.utils.command_type import CommandType
from serverpanel.models import Server, Game, Configuration, Command, Parameters
from .utils import downloader
from .utils import files
from .utils import unzipper
from .utils import user_utils
from .utils.sub_server import SubServer
from django.contrib.auth.decorators import login_required


running_servers = {}

@login_required(login_url='/users/login')
def panel_server_list(request):
    try:
        paneluser = PanelUser.objects.get(user=request.user)
        servers = Server.objects.all().filter(owner=paneluser)
        return render(request, 'server-list.html', {'servers': servers, 'paneluser': paneluser})
    except PanelUser.DoesNotExist:
        return render(request, 'server-list.html', {})

@login_required(login_url='/users/login')
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

@login_required(login_url='/users/login')   
def panel_server_start(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        if f"{id}" in running_servers:
            return JsonResponse({'message': 'Le serveur est déjà démarré.'})
        else:
            server = Server.objects.get(id=id)
            sub_server = SubServer(
                os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, server.directory), 
                server.max_ram, 
                server.start_command, 
                server.stop_command,
                server.game,
                server.parameters.all())
            done = sub_server.start_server()
            if done:
                running_servers[f"{id}"] = sub_server
                return JsonResponse({'message': 'Le serveur a bien été démarré.'})
            else:
                return JsonResponse({'message': 'Le serveur n\'a pas pu être demarré.'})
    else:
        return render(request, 'server-not-accessible.html')

@login_required(login_url='/users/login')
def panel_server_stop(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        if f"{id}" in running_servers:
            server = running_servers[f"{id}"]
            done = server.stop_server()
            if done:
                del running_servers[f"{id}"]
                return JsonResponse({'message': 'Le serveur a bien été arrêté.'})
            else:
                return JsonResponse({'message': 'Le serveur n\'a pas pu être arrêté.'})
        return JsonResponse({'message': 'Le serveur n\'est pas demarré.'})
    else:
        return render(request, 'server-not-accessible.html')

@login_required(login_url='/users/login')
def panel_server_cmd(request, id, cmd):
    if user_utils.do_user_have_access_to_server(request.user, id):
        if f"{id}" in running_servers:
            server = running_servers[f"{id}"]
            if server.game.name == "Minecraft":
                done = server.send_command(cmd)
                if done:
                    return JsonResponse({'message': 'La commande a bien été envoyée.'})
                else:
                    return JsonResponse({'message': 'Impossible d''envoyer la commande.'})
            else:
                    return JsonResponse({'message': 'Impossible d''envoyer une commande dans ce type de serveur.'})
        else:
            return JsonResponse({'message': 'Impossible d''envoyer la commande.'})
    else:
        return render(request, 'server-not-accessible.html')

@login_required(login_url='/users/login')
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
        
        if f"{id}" not in running_servers:
            sub_server = SubServer(
                os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, server.directory), 
                server.max_ram, 
                server.start_command, 
                server.stop_command,
                server.game,
                server.parameters.all())
            sub_server.install_server()



        return JsonResponse({'message': 'Le serveur a bien été installé.'})
    else:
        return render(request, 'server-not-accessible.html')

@login_required(login_url='/users/login')
def panel_server_logs(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        try:
            server = Server.objects.get(id=id)
            try:
                logs_file = files.get_latest_log_file(os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, server.directory))
                if logs_file is None:
                    return JsonResponse({'logs': 'Aucun fichier logs trouvé !'})
                else:
                    with open(logs_file, 'r') as fichier:
                        try:
                            logs = fichier.read()
                            return JsonResponse({'logs': logs})
                        except UnicodeDecodeError:
                            return JsonResponse({'logs': 'Aucun fichier logs trouvé !'})
            except FileNotFoundError:
                return JsonResponse({'logs': 'Aucun fichier logs trouvé !'})
        except Server.DoesNotExist:
            return JsonResponse({'logs': 'Aucun fichier logs trouvé !'})
    else:
        return render(request, 'server-not-accessible.html')

@login_required(login_url='/users/login')
def panel_server_delete(request, id):
    if user_utils.do_user_have_access_to_server(request.user, id):
        if f"{id}" in running_servers:
            server = running_servers[f"{id}"]
            paneluser = PanelUser.objects.get(user=request.user)
            servers = Server.objects.all().filter(owner=paneluser)
            return JsonResponse({'message': "Veuillez arrêter le serveur avant de le supprimer."}, status=400)
        server = Server.objects.get(id=id)
        server_path = os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, server.directory)
        shutil.rmtree(server_path)
        parameters = server.parameters.all()
        for parameter in parameters:
            parameter.delete()
        server.delete()
        paneluser = PanelUser.objects.get(user=request.user)
        servers = Server.objects.all().filter(owner=paneluser)
        return render(request, 'server-list.html', {'servers': servers, 'paneluser': paneluser})
    else:
        return render(request, 'server-not-accessible.html')
    
    
@login_required(login_url='/users/login')
def panel_server_create(request):
    if request.method == 'POST':
        form = CreateServerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            game = form.cleaned_data['game']
            configuration = form.cleaned_data['configuration']
            ram = form.cleaned_data['max_ram']

            game = Game.objects.get(name=game)
            configuration = Configuration.objects.get(name=configuration)
            start_command = None
            stop_command = None
            
            commands = Command.objects.all()
            for command in commands:
                if "Start" in command.name and game.name in command.name:
                    start_command = command
                if "Stop" in command.name and game.name in command.name:
                    stop_command = command

            server = Server()
            server.name = name
            server.game = game
            server.start_command = start_command
            server.stop_command = stop_command
            server.configuration = configuration
            server.max_ram = ram
            server.directory = request.user.username + "/" + uuid.uuid4().hex
            server.save()
            
            # Add selected users to the server
            paneluser = PanelUser.objects.get(user=request.user)
            servers = Server.objects.all().filter(owner=paneluser)
            selected_users = PanelUser.objects.filter(user=request.user)
            server.owner.add(*selected_users)

            #Add selected parameters to the server
            if game.name in "Minecraft":
                parameter = Parameters()
                parameter.name = "--port "
                parameter.port = random.randint(1025, 65535)
                parameter.server = server
                parameter.save()
                server.parameters.add(parameter)
            if game.name in "Teamspeak":
                parameter = Parameters()
                parameter.name = "default_voice_port="
                parameter.port = random.randint(1025, 65535)
                parameter.server = server
                parameter.save()
                server.parameters.add(parameter)
                parameter = Parameters()
                parameter.name = "filetransfer_port="
                parameter.port = random.randint(1025, 65535)
                parameter.server = server
                parameter.save()
                server.parameters.add(parameter)
                parameter = Parameters()
                parameter.name = "query_port="
                parameter.port = random.randint(1025, 65535)
                parameter.server = server
                parameter.save()
                server.parameters.add(parameter)
                parameter = Parameters()
                parameter.name = "query_ssh_port="
                parameter.port = random.randint(1025, 65535)
                parameter.server = server
                parameter.save()
                server.parameters.add(parameter)
                parameter = Parameters()
                parameter.name = "query_http_port="
                parameter.port = random.randint(1025, 65535)
                parameter.server = server
                parameter.save()
                server.parameters.add(parameter)
            return render(request, 'server-list.html', {'servers': servers, 'paneluser': paneluser})
    else:
        form = CreateServerForm()
        games = Game.objects.all()
        configurations = Configuration.objects.all()
    return render(request, 'server-create.html', {
        'form': form,
        'games': games,
        'configurations': configurations})