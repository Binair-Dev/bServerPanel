from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class PanelUser(models.Model):
    username = models.CharField(max_length=255, unique=True, default=None)
    email = models.EmailField(max_length=255, unique=True, default=None)
    password = models.CharField(max_length=255, default=None)
    rank = models.ManyToManyField('serverpanel.Rank')
    is_superuser = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)
    server_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"