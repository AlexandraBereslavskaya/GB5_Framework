from time import time
from patterns.creational_patterns import Logger

"""Структурные паттерны"""

"""Декоратор — это структурный паттерн проектирования, 
    который позволяет динамически добавлять объектам новую функциональность, 
    оборачивая их в полезные «обёртки»."""

logger = Logger('main')


class FrameRoute:

    def __init__(self, routes_dict, url):
        self.routes_dict = routes_dict
        self.url = url

    # Декоратор. При вызове обновляет словарь маршрутов.
    def __call__(self, cls):
        self.routes_dict[self.url] = cls()


class FrameDebug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def time_decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time()
                func_result = func(*args, **kwargs)
                end_time = time()
                time_interval = end_time - start_time
                message = f' Debug >>> {self.name} выполнялась {time_interval:2.3f} ms'
                logger.log(message)
                return func_result

            return wrapper
        return time_decorator(cls)
