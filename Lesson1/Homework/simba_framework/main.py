import quopri
from time import time


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj
        self.statistic_time = int(time())
        self.statistic_dict = {}

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        if path in self.statistic_dict:
            self.statistic_dict[path] += 1
        else:
            self.statistic_dict.setdefault(path, 1)
        self.get_statistic()

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
        request = {}
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def get_statistic(self):
        if int(time()) - self.statistic_time >= 3600:
            print("Статистика посещения страниц за последний час: ", self.statistic_dict)
            self.statistic_time = int(time())
            self.statistic_dict.clear()
