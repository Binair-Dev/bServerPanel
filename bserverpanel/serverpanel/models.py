from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import AbstractBaseUser
    
class PanelUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, default=None)
    email = models.EmailField(max_length=255, unique=True, default=None)
    password = models.CharField(max_length=255, default=None)
    rank = models.ManyToManyField('Rank')
    is_superuser = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)
    server_count = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        if self.password:
            # Vérifie si l'objet est nouveau ou si le mot de passe a été modifié
            if not self.pk or self._password != self.password:
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} | {self.email}"

class Server(models.Model):
    owner = models.ManyToManyField(PanelUser)
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
    user = models.ManyToManyField(PanelUser)

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