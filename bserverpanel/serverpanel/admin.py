from re import A
from django.contrib import admin
from serverpanel.models import Server, Game, Transaction, Command, Configuration
# Register your models here.

admin.site.register(Server)
admin.site.register(Game)
admin.site.register(Transaction)
admin.site.register(Command)
admin.site.register(Configuration)