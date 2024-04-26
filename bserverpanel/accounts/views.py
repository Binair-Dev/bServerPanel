from django.shortcuts import render
from django.shortcuts import render, redirect
from accounts.forms import RegisterPanelUserForm
from accounts.forms import LoginPanelUserForm
from accounts.models import PanelUser
from serverpanel.models import Rank
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout

# Create your views here.
def panel_user_list(request):
    return render(request, 'user-list.html', {'users': PanelUser.objects.all()})

def panel_user_login(request):
    if request.method == 'POST':
        form = LoginPanelUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = PanelUser.objects.get(username=username)
            if check_password(password, user.password):
                return redirect('index')
            else:
                return render(request, 'user-login.html', {'form': form})
    else:
        form = LoginPanelUserForm()
        return render(request, 'user-login.html', {'form': form})
    
def panel_user_register(request):
    if request.method == 'POST':
        form = RegisterPanelUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if password == password_confirm:
                try:
                    rank = Rank.objects.get(name='Membre')
                except Rank.DoesNotExist:
                    rank = Rank.objects.create(name='Membre')

                rank = Rank.objects.get(name='Membre')
                panelUser = PanelUser.objects.create(username=username, email=email, password=password, is_superuser=False, balance=0, is_deleted=False, server_count=0)
                panelUser.rank.add(rank)
                return redirect('index')
            else:
                return render(request, 'user-register.html', {'form': form})
    else:
        form = RegisterPanelUserForm()
        return render(request, 'user-register.html', {'form': form})
    
def panel_user_logout(request):
    logout(request)
    return redirect('index')