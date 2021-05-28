from wsgiref.simple_server import make_server
from simba_framework.main import Framework, FakeFramework, DebugFramework
from urls import fronts
from views import routes_dict

application = Framework(routes_dict, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
