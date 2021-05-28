from copy import deepcopy
from quopri import decodestring
import json

from patterns.behavioral_patterns import Observed, FileWriter, ConsoleWriter


"""Порождающие паттерны"""


"""
Синглтон (одиночка) - это порождающий паттерн проектирования, 
который гарантирует, что у класса есть только один экземпляр, и предоставляет к нему глобальную точку доступа.
"""


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        # если данный экземпляр еще НЕ существует, то мы его создаем
        if name not in cls.__instance:
            cls.__instance[name] = super().__call__(*args, **kwargs)

        return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, message):
        message = f"LOG>>> {message}"
        self.writer.write_out(message)


logger = Logger('main')


"""
Абстрактная фабрика -Абстрактная фабрика — это порождающий паттерн проектирования, 
который позволяет создавать семейства связанных объектов, не привязываясь к конкретным классам создаваемых объектов.
"""


# абстрактный пользователь
class User:

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


"""!!! Вот тут я буду избавляться от антипатерна. ))"""
class Professional(User):
    pass
"""
    def __init__(self, name: str, speciality: str, school: str):
        self.name = name
        self.speciality = speciality
        self.school = school

        professionals_dict = {}

        try:
            input_json = open("data/professions.json")
            professionals_dict = json.load(input_json)
            print(professionals_dict)
            input_json.close()
        except IOError:
            print("Файл не найден")

        professionals_dict[self.school][self.name] = self.speciality
        print(professionals_dict)

        try:
            input_json = open("data/professions.json", "w", encoding='utf-8')
            json.dump(professionals_dict, input_json, ensure_ascii=False)
            input_json.close()
        except IOError:
            print("Файл не найден")
"""


class Student(User):

    def __init__(self, name, email, phone):
        self.courses = []
        super().__init__(name, email, phone)

    def add_course(self, course):
        self.courses.append(course)


# Создаем фабрику пользователей:
class UserFactory:
    user_types = {"professional": Professional, "student": Student}

    @classmethod
    def create(cls, user_type, name, email, phone):
        return cls.user_types[user_type](name, email, phone)


"""
Прототип — это порождающий паттерн проектирования, 
который позволяет копировать объекты, не вдаваясь в подробности их реализации.
"""


class CoursePrototype:

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Observed):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        # вносим курс в список курсов категории
        self.category.courses.append(self)
        self.students = []
        print("__init__Course", len(self.category.courses))

    def create_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()



class Category:
    # создаем записи для
    generated_id = 0

    def __init__(self, name):
        self.category_id = Category.generated_id
        Category.generated_id += 1
        self.name = name
        self.courses = []

    def course_number(self):
        return len(self.courses)


class InteractiveCourse(Course):
    pass


class WebinarCourse(Course):
    pass


class RecordedCourse(Course):
    pass


class MiniGroup(Course):
    pass


# Создаем фабрику курсов
class CourseFactory:
    course_types = {"interactive": InteractiveCourse,
                    "webinar": WebinarCourse,
                    "recorded": RecordedCourse,
                    "mini_group": MiniGroup}

    @classmethod
    def create(cls, user_type, name, category):
        return cls.course_types[user_type](name, category)


# Движок - интерфейс проекта
class Engine:
    def __init__(self):
        self.professionals = []
        self.students = []
        self.categories = []
        self.courses = []
        self.areas = []

    # создаем пользователя (преподаватель/студент) используя абстрактную фабрику
    @staticmethod
    def create_user(user_type, name, email, phone):
        return UserFactory.create(user_type, name, email, phone)

    @staticmethod
    def create_area(name, city, address, phone_number):
        return Area(name, city, address, phone_number)

    # создаем категорию (интерактивный/вебинар/курс_в_записе/мини-групповой)
    # использую соответствующую абстрактную фабрику
    @staticmethod
    def create_category(name):
        return Category(name)

    # поиск категории по "ключу"
    def find_category_by_id(self, category_id):
        logger.log("Поиск категории по ключу")
        for item in self.categories:
            if item.category_id == category_id:
                return item
        raise Exception(f'Нет категории с id = {category_id}')

    # создание курса
    @staticmethod
    def create_course(type_, name, category):
        print(type_, name, category.name)
        return CourseFactory.create(type_, name, category)

    # вытаскиваем курс по имени обходим в цикле весь список курсов
    def get_course(self, name):
        logger.log(f"Вытаскиваем курс {name}")
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_all_courses(self):
        logger.log(f"Полный список курсов")
        print(self.courses)
        return self.courses

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class Area:

    def __init__(self, name, city, address, phone_number):
        self.name = name
        self.city = city
        self.address = address
        self.phone_number = phone_number
        # self.courses = [] - это надо доделовать. Добавлять связку с Area к курсу.
