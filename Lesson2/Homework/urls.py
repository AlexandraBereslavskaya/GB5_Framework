from datetime import date
from views import Index, Professionals, Contacts, About


# front controller
def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/index/': Index(),
    '/professionals/': Professionals(),
    '/contacts/': Contacts(),
    '/about/': About()
}
