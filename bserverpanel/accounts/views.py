from django.shortcuts import render, redirect
from accounts.forms import RegisterPanelUserForm
from accounts.forms import LoginPanelUserForm
from accounts.models import PanelUser
from utils.decoder import isAuthenticated
from accounts.models import Rank
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

# Create your views here.
def panel_user_list(request):
    is_authenticated = isAuthenticated(request)
    if is_authenticated:
        return render(request, 'user-list.html', {'users': PanelUser.objects.all()})
    else:
        return redirect('/users/login')

def panel_user_login(request):
    if request.method == 'POST':
        form = LoginPanelUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                return redirect('user-login')
    return render(request, 'user-login.html', {'form': LoginPanelUserForm})

def panel_user_register(request):
    if request.method == 'POST':
        form = RegisterPanelUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if password == password_confirm:
                user, created = User.objects.get_or_create(username=username, email=email, defaults={'password': make_password(password), 'is_superuser': False})
                
                if created:
                    rank, _ = Rank.objects.get_or_create(name='Membre')
                    panel_user = PanelUser.objects.create(balance=0, server_count=0, user=user)
                    panel_user.rank.add(rank)
                    return redirect('index')
                else:
                    return render(request, 'user-register.html', {'form': form, 'message': 'Un utilisateur de ce nom existe déjà'})
            else:
                return render(request, 'user-register.html', {'form': form})
    else:
        form = RegisterPanelUserForm()
        return render(request, 'user-register.html', {'form': form})

    
def panel_user_logout(request):
    logout(request)
    return redirect('index')