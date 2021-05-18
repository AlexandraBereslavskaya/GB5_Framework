from simba_framework.templator import render
from data.framework_data import SPECIALIST_DICT


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class Professionals:
    def __call__(self, request):
        return '200 OK', render('professionals.html', object_dict=SPECIALIST_DICT)


class About:
    def __call__(self, request):
        return '200 OK', 'The page is being finalized'


class Contacts:
    def __call__(self, request):
        return '200 OK', 'The page is being finalized'


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
