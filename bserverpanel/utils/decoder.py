from django.conf import settings
from accounts.models import PanelUser
import jwt

#Added custom decoder for authentication
def login(request):
    token = request.COOKIES.get('jwt')
    if token:
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token['user_id']
            user = PanelUser.objects.get(pk=user_id)
            request.user = user
        except Exception as e:
            return None
    else:
        return None
    
def isAuthenticated(request):
    login(request)
    if request.user is not None and request.user.username != "":
        return True
    else:
        return False