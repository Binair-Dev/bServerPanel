from django.db import models

# Create your models here.
class PanelUser(models.Model):
    rank = models.ManyToManyField('serverpanel.Rank', default=None)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    server_count = models.IntegerField(default=0)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.username}"