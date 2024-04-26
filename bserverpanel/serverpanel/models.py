from django.db import models
from django.contrib.auth.models import Permission

class Server(models.Model):
    owner = models.ManyToManyField('accounts.PanelUser')
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    configuration = models.ManyToManyField('Configuration')
    max_ram = models.IntegerField()
    storage_amount = models.IntegerField()
    start_command = models.CharField(max_length=255)
    stop_command = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} | {self.game.name}"

class Game(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
        
class Rank(models.Model):
    name = models.CharField(max_length=255)
    permission = models.ManyToManyField(Permission)

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
    position = models.IntegerField()
    command_line = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.command_line}"
    
class Configuration(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    commands = models.ManyToManyField(Command)

    def __str__(self):
        return f"{self.name}: {self.value}"