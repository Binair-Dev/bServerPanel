from django import forms
from serverpanel.models import Configuration, Game, Server

class CreateServerForm(forms.Form):
    name = forms.CharField(max_length=255)
    game = forms.ModelChoiceField(queryset=Game.objects.all())
    configuration = forms.ModelChoiceField(queryset=Configuration.objects.all())
    max_ram = forms.IntegerField()
    
    class Meta:
        model = Server
        fields = ['name', 'game', 'configuration', 'max_ram']