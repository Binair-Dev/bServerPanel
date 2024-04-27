from django.shortcuts import render, redirect
from accounts.forms import RegisterPanelUserForm
from accounts.forms import LoginPanelUserForm
from accounts.models import PanelUser
from utils.decoder import isAuthenticated
from serverpanel.models import Rank
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.urls import reverse

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
            try:
                user = PanelUser.objects.get(username=username)
            except PanelUser.DoesNotExist:
                return render(request, 'user-login.html', {'form': form, 'message': "Ce nom d'utilisateur n'existe pas"})
            user = PanelUser.objects.get(username=username)
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                # refresh['custom_data'] = {
                #     'user_id': user.id,
                #     'username': user.username,
                #     'rank': user.rank.first().name,
                # }
                
                response = HttpResponseRedirect(reverse('index'))
                response.set_cookie('jwt', str(refresh.access_token), httponly=True)
                return response
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
                try:
                    panelUser = PanelUser.objects.create(username=username, email=email, password=password, is_superuser=False, balance=0, is_deleted=False, server_count=0)
                    panelUser.rank.add(rank)
                    return redirect('index')
                except:
                    return render(request, 'user-register.html', {'form': form, 'message': 'Un utilisateur de ce nom existe de déjà'})
            else:
                return render(request, 'user-register.html', {'form': form})
    else:
        form = RegisterPanelUserForm()
        return render(request, 'user-register.html', {'form': form})
    
def panel_user_logout(request):
    response = redirect('index')
    response.delete_cookie('jwt')
    response.delete_cookie('sessionid')
    return response