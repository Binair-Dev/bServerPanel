from accounts.models import PanelUser
from serverpanel.models import Server

def do_user_have_access_to_server(user, id):
    try:
        panel_user = PanelUser.objects.get(user=user)
        server = Server.objects.all().filter(owner=panel_user)
        for s in server:
            if s.id == id:
                return True
        return False
    except PanelUser.DoesNotExist:
        return False
    except Server.DoesNotExist:
        return False