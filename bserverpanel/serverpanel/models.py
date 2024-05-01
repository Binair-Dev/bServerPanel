from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=255, default="server")
    directory = models.CharField(max_length=255, default=None, null=True)
    owner = models.ManyToManyField('accounts.PanelUser')
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    configuration = models.ForeignKey('Configuration', on_delete=models.CASCADE, default=None, null=True)
    max_ram = models.IntegerField(default=2)
    start_command = models.ForeignKey('Command', on_delete=models.SET_NULL, related_name="start_command", default=None, null=True)
    stop_command = models.ForeignKey('Command', on_delete=models.SET_NULL, related_name="stop_command", default=None, null=True)
    parameters = models.ManyToManyField('Parameters')

    def __str__(self):
        return f"{self.id} | {self.game.name}"

class Game(models.Model):
    name = models.CharField(max_length=255)
    stop_type = models.CharField(max_length=255, default="OS_COMMAND - PROGRAM_COMMAND")
    stop_command = models.CharField(max_length=255, default="stop")

    def __str__(self):
        return f"{self.name}"

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=255)
    user = models.ManyToManyField('accounts.PanelUser')

    def __str__(self):
        return f"{self.id}"
    
class Command(models.Model):
    name = models.CharField(max_length=255, default="")
    command_type = models.CharField(max_length=255, default="")
    position = models.IntegerField()
    link = models.CharField(max_length=255, default="none")
    file_name = models.CharField(max_length=255, default="none")
    command_line = models.CharField(max_length=255, default="none")

    def __str__(self):
        return f"{self.name}"
    
class Configuration(models.Model):
    name = models.CharField(max_length=255)
    commands = models.ManyToManyField(Command)

    def __str__(self):
        return f"{self.name}"
    
class Parameters(models.Model):
    name = models.CharField(max_length=255, default="default-port")
    port = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name}"