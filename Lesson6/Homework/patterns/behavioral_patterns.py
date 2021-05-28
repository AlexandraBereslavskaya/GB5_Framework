from jsonpickle import dumps, loads
from simba_framework.templator import render

""" Поведенческие паттерны """


""" Наблюдатель — это поведенческий паттерн проектирования, 
    который создаёт механизм подписки, позволяющий 
    одним объектам следить и реагировать на события, происходящие в других объектах."""


# класс наблюдатель
class Observer:

    def update(self, observed):
        pass


# класс наблюдаемый
class Observed:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, observed):
        print("SMS>>> новый студент", observed.students[-1].name)


class CallNotifier(Observer):
    def update(self, observed):
        print("CALL>>> новый студент", observed.students[-1].name)


class EmailNotifier(Observer):
    def update(self, observed):
        print("EMAIL>>> новый студент", observed.students[-1].name)


"""Встроенный способ сериализации и десериализации объектов в Python"""
class PickleSerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


""" Стратегия — это поведенческий паттерн проектирования, который определяет семейство схожих алгоритмов
    и помещает каждый из них в собственный класс, 
    после чего алгоритмы можно взаимозаменять прямо во время исполнения программы.
    Применяем ее для логирования
"""
class FileWriter:

    def __init__(self, file_name):
        self.file_name = file_name

    def write_out(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as file_stream:
            file_stream.write(f"{text} \n")


class ConsoleWriter:

    def write_out(self, text):
        print(text)


""" Шаблонный метод — это поведенческий паттерн проектирования, 
    который определяет скелет алгоритма, перекладывая ответственность за некоторые его шаги на подклассы. 
    Паттерн позволяет подклассам переопределять шаги алгоритма, не меняя его общей структуры."""


# в django обрабатывает заданный шаблон, используя контекст (context), содержащий параметры из URL
# определяет наши шаги выполняемые в ходе приложения.
class TemplateView:
    template_name = 'template.html'

    # контекст передаваемые в шаблон динамически
    def get_context_data(self):
        return {}

    # формируем сам шаблон
    def get_template(self):
        return self.template_name

    # порядок шаблонных методов.
    def render_template_context(self):
        template_name = self.get_template()
        print(template_name)
        context = self.get_context_data()
        return "200 OK", render(template_name, **context)

    def __call__(self, request):
        return self.render_template_context()


# класс контроллер для обработки вывода списка чего-то: категорий, заказа, товара и т.д.
# задача получать массив чего-нибудь и передавать его в сам шаблон
class ListView(TemplateView):
    query_set = []
    template_name = 'list.html'
    context_obj_name = 'objects_list'

    def get_query_set(self):
        return self.query_set

    def get_context_obj_name(self):
        return self.context_obj_name

    def get_context_data(self):
        query_set = self.get_query_set()
        context_obj_name = self.get_context_obj_name()
        context = {context_obj_name: query_set}
        return context


# отработка механизма Создания чего-то: категорий, заказа, товара и т.д.
class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            # визуализация шаблона
            return self.render_template_context()
        else:
            return super().__call__(request)
