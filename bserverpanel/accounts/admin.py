from django.contrib import admin
from .models import PanelUser, Rank

# Register your models here.
admin.site.register(PanelUser)
admin.site.register(Rank)