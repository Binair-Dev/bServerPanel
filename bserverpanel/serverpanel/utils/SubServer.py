import subprocess
import time
import atexit

class SubServer:
    def __init__(self, server_path, max_ram, start_command, stop_command):
        self.server_path = server_path
        self.process = None
        self.max_ram = max_ram
        self.start_command = start_command
        self.stop_command = stop_command

        atexit.register(self.close_server)
    
    def start_server(self):
        if not self.process:
            try:
                self.process = subprocess.Popen(self.start_command.replace("%RAM%", str(self.max_ram)), cwd=self.server_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            except Exception as e:
                return False
        else:
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
            try:
                self.send_command(self.stop_command)
                print("Arrêt en cours des serveurs")
                self.process.wait(timeout=10)
                print("Arrêt terminé")
            except subprocess.TimeoutExpired:
                print("Erreur lors de l'arrêt des serveurs")
                self.process.terminate()
                self.process.wait()