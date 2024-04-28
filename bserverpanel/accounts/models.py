from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.
class Rank(models.Model):
    name = models.CharField(max_length=255)
    permission = models.ManyToManyField(Permission, default=None)

    def __str__(self):
        return f"{self.name}"
    
class PanelUser(models.Model):
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    server_count = models.IntegerField(default=0)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user}"
    