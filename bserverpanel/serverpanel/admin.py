from re import A
from django.contrib import admin
from serverpanel.models import PanelUser, Server, Game, Rank, Transaction, Command, Configuration
# Register your models here.

admin.site.register(PanelUser)
admin.site.register(Server)
admin.site.register(Game)
admin.site.register(Rank)
admin.site.register(Transaction)
admin.site.register(Command)
admin.site.register(Configuration)