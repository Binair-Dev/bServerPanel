from os import name
from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default(sender, **kwargs):
    from .models import Game, Command, Configuration
    if Game.objects.count() == 0:
        Game.objects.create(
            name="Minecraft", 
            stop_type="PROGRAM_COMMAND", 
            stop_command="stop")
        Game.objects.create(
            name="Teamspeak", 
            stop_type="KILL", 
            stop_command="kill $(cat teamspeak3-server_linux_amd64/ts3server.pid)")
    if Command.objects.count() == 0:
        # Création des objets Command
        download_papermc_command = Command.objects.create(
            name="Download PaperMC 1.20.4", 
            command_type="LINK",
            position=0,
            link="https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/496/downloads/paper-1.20.4-496.jar",
            file_name="server.jar",
            command_line="none")
        accept_eula_command = Command.objects.create(
            name="Accepter EULA", 
            command_type="ACCEPT_EULA",
            position=1,
            link="none",
            file_name="none",
            command_line="none")
        download_teamspeak_command = Command.objects.create(
            name="Download Teamspeak3 3.13.7", 
            command_type="LINK",
            position=0,
            link="https://files.teamspeak-services.com/releases/server/3.13.7/teamspeak3-server_linux_amd64-3.13.7.tar.bz2",
            file_name="teamspeak3-server_linux_amd64-3.13.7.tar.bz2",
            command_line="none")
        unzip_teamspeak_command = Command.objects.create(
            name="Unzip Teamspeak3", 
            command_type="UNZIP",
            position=1,
            link="none",
            file_name="teamspeak3-server_linux_amd64-3.13.7.tar.bz2",
            command_line="none")
        start_minecraft_command = Command.objects.create(
            name="Start Minecraft", 
            command_type="OS_COMMAND",
            position=0,
            link="none",
            file_name="none",
            command_line="java -Xmx%RAM%G -jar server.jar %PARAMETERS% --nogui")
        stop_minecraft_command = Command.objects.create(
            name="Stop Minecraft", 
            command_type="PROGRAM_COMMAND",
            position=1,
            link="none",
            file_name="none",
            command_line="stop")
        start_teamspeak_command = Command.objects.create(
            name="Start Teamspeak", 
            command_type="OS_COMMAND",
            position=0,
            link="none",
            file_name="none",
            command_line="./teamspeak3-server_linux_amd64/ts3server_minimal_runscript.sh license_accepted=1 createinifile=1 serveradmin_password=serveradmin %PARAMETERS%")
        stop_teamspeak_command = Command.objects.create(
            name="Stop Teamspeak", 
            command_type="KILL",
            position=1,
            link="none",
            file_name="none",
            command_line="none")

        # Création des objets Configuration avec les objets Command
        if Configuration.objects.count() == 0:
            teamspeak_commands = [download_teamspeak_command, unzip_teamspeak_command]
            minecraft_commands = [download_papermc_command, accept_eula_command]

            teamspeak_config = Configuration.objects.create(name="Teamspeak 3")
            minecraft_config = Configuration.objects.create(name="Minecraft")

            teamspeak_config.commands.set(teamspeak_commands)
            minecraft_config.commands.set(minecraft_commands)


class ServerpanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'serverpanel'

    def ready(self):
        post_migrate.connect(create_default, sender=self)