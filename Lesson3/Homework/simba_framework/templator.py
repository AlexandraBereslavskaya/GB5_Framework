from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """

    environment = Environment()
    environment.loader = FileSystemLoader(folder)
    # Открываем шаблон по имени
    template = environment.get_template(template_name)
    # рендерим шаблон с параметрами
    return template.render(**kwargs)
