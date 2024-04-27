import subprocess

def execute_commands(commands):
    for command in commands:
        subprocess.run(command, shell=True)