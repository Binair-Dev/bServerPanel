import subprocess
import time
import atexit

from serverpanel.utils.command_type import CommandType

class SubServer:
    def __init__(self, server_path, max_ram, start_command, stop_command, game):
        self.server_path = server_path
        self.process = None
        self.max_ram = max_ram
        self.start_command = start_command
        self.stop_command = stop_command
        self.game = game

        atexit.register(self.close_server)
    
    def start_server(self):
        if not self.process:
            try:
                command_list = self.start_command.replace("%RAM%", str(self.max_ram)).split()
                self.process = subprocess.Popen(command_list, cwd=self.server_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            except Exception as e:
                return False
        else:
            return False

    def stop_server(self):
        if self.game.stop_type in CommandType.PROGRAM_COMMAND.value:
            print(self.game.stop_command)
            self.send_command(self.stop_command)
            return True
        if self.game.stop_type in CommandType.KILL.value:
            self.process.terminate()
            self.process.wait()
            return True
        return False
    
    def restart_server(self):
        self.send_command(self.stop_command)
        time.sleep(5)
        self.start_server()
        return True
    
    def send_command(self, command):
        if self.process:
            self.process.stdin.write(command.encode("utf-8") + b"\n")
            self.process.stdin.flush()
            return True
        else:
            return False

    def close_server(self):
        if self.process:
            print("Arrêt en cours des serveurs")
            try:
                if self.game.name in "Teamspeak":
                    with open(self.server_path + "/teamspeak3-server_linux_amd64/ts3server.pid", 'r') as file:
                        pid = int(file.read().strip())
                        command_list = str("kill " + str(pid)).split()
                        self.process = subprocess.Popen(command_list, cwd=self.server_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                        self.process.wait(timeout=5)
                        self.process.terminate()
                        self.process.wait()
                        print("Arrêt terminé")
                        return True
                if self.game.name in "Minecraft":
                    self.send_command(self.stop_command)
                    self.process.wait(timeout=5)
                    self.process.terminate()
                    self.process.wait()
                    print("Arrêt terminé")
            except subprocess.TimeoutExpired:
                self.process.terminate()
                self.process.wait()