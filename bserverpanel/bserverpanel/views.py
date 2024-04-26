from django.shortcuts import render
import jwt

def index(request):
    token = request.COOKIES.get('jwt')
    if jwt is not None:
        try:
            decoded_token = jwt.decode(token, 'django-insecure-8hh$)^ft!oz3cptcre2nrf2xipu^ybhoinipqfh2u_h4!ao*bb', algorithms=['HS256'])
            # user_id = decoded_token['user_id']
            return render(request, 'index.html')
        except Exception as e:
            return render(request, 'index.html')
    return render(request, 'index.html')