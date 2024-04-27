from django.shortcuts import render
from django.shortcuts import redirect
from utils.decoder import isAuthenticated

def index(request):
    is_authenticated = isAuthenticated(request)
    if is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('/users/login')