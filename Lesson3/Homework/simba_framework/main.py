import quopri
from time import time
from json import dump
from simba_framework.requests import GetRequests, PostRequests
from variables.variables import STATISTIC_PERIOD, CLIENT_INPUT_FILE


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

        request = {}
        method = environ["REQUEST_METHOD"]
        request["method"] = method
        if method == "POST":
            data = PostRequests().get_params(environ)
            request["data"] = data
            print(f"Получен Post-запрос: {Framework.decode_value(data)}")
            Framework.update_data_file({method: Framework.decode_value(data)})
        if method == "GET":
            request_params = GetRequests().get_params(environ)
            request["request_params"] = request_params
            if request_params:
                print(f"Получены Get-параметры: {request_params}")
                Framework.update_data_file({method: request_params})

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
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
        if int(time()) - self.statistic_time >= STATISTIC_PERIOD:
            print("Статистика посещения страниц за последний час: ", self.statistic_dict)
            self.statistic_time = int(time())
            self.statistic_dict.clear()

    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data

    @staticmethod
    def update_data_file(input_update: dict):
        try:
            input_json = open(CLIENT_INPUT_FILE, "a", encoding='utf-8')
            dump(input_update, input_json, ensure_ascii=False)
            input_json.close()
        except IOError:
            print("Файл не найден")
