from simba_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from data.framework_data import SPECIALIST_DICT
from patterns.structural_patterns import FrameRoute, FrameDebug
from patterns.behavioral_patterns import EmailNotifier, CallNotifier, SmsNotifier, PickleSerializer, \
    ListView, CreateView


site = Engine()
logger = Logger('main')

routes_dict = {}


@FrameRoute(routes_dict=routes_dict, url='/')
class Index:

    @FrameDebug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@FrameRoute(routes_dict=routes_dict, url='/schedule/')
class Schedule:

    @FrameDebug(name='Schedule')
    def __call__(self, request):
        return '200 OK', render('schedule.html', data=request.get('data', None))


@FrameRoute(routes_dict=routes_dict, url='/professionals/')
class Professionals:

    @FrameDebug(name='Professionals')
    def __call__(self, request):
        return '200 OK', render('professionals.html', object_dict=SPECIALIST_DICT)


@FrameRoute(routes_dict=routes_dict, url='/about/')
class About:

    @FrameDebug(name='About')
    def __call__(self, request):
        return '200 OK', 'The page is being finalized'


class NotFound404:

    @FrameDebug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@FrameRoute(routes_dict=routes_dict, url='/course-list/')
class CoursesList:

    @FrameDebug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        if 'id' in request['request_params']:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course-list.html', objects_list=category.courses,
                                    name=category.name, category_id=category.category_id)
        else:
            try:
                courses_obj_list = site.get_all_courses()
                courses_list = []
                for course in courses_obj_list:
                    course_dict = {'course_name': course.name, 'course_category': course.category.name}
                    courses_list.append(course_dict)

                return '200 OK', render('course-list.html', objects_list=courses_list)

            except KeyError:
                return '202 OK', 'No courses found'


@FrameRoute(routes_dict=routes_dict, url='/course-creation/')
class CourseCreation:
    category_id = -1

    @FrameDebug(name='CourseCreation')
    def __call__(self, request):
        logger.log('Создание курса')
        if request['method'] == 'POST':
            logger.log("Post method")
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('recorded', name, category)
                site.courses.append(course)

            return '200 OK', render('course-list.html', objects_list=category.courses,
                                    name=category.name, category_id=category.category_id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                course_name = None
                # имя дублирующегося курса
                if 'course_name' in request['request_params']:
                    course_name = request['request_params']['course_name']
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('course-creation.html', objects_list=category.courses, name=category.name,
                                        id=category.category_id, course_name=course_name)
            except KeyError:
                return '200 OK', 'No categories found'


@FrameRoute(routes_dict=routes_dict, url='/course-copy/')
class CourseCopy:

    @FrameDebug(name='CourseCopy')
    def __call__(self, request):
        logger.log('Копирование курса')
        request_params = request['request_params']

        try:
            name = request_params['name']
            previous_course = site.get_course(name)
            if previous_course:
                next_name = f'copy_{name}'
                new_course = previous_course.clone()
                new_course.name = next_name
                site.courses.append(new_course)

            return '200 OK', render('course-list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses found'


@FrameRoute(routes_dict=routes_dict, url='/category-creation/')
class CategoryCreation:

    @FrameDebug(name='CategoryCreation')
    def __call__(self, request):
        logger.log('Создание категории')
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name)
            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            return '200 OK', render('category-creation.html', categories=site.categories)


@FrameRoute(routes_dict=routes_dict, url='/category-list/')
class CategoryList:

    @FrameDebug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html', objects_list=site.categories)


@FrameRoute(routes_dict=routes_dict, url='/new-student/')
class NewStudent:

    @FrameDebug(name='NewStudent')
    def __call__(self, request):
        logger.log('Регистрация студента')

        students_list = []

        if request['method'] == 'GET':
            data = request['request_params']
            course_name = data['course_name']

        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            email = data['email']
            email = site.decode_value(email)

            phone = data['phone']
            phone = site.decode_value(phone)

            course_name = data['course_name']
            course_name = site.decode_value(course_name)

            new_student = site.create_user('student', name, email, phone)
            course = site.get_course(course_name)
            new_student.add_course(course)
            site.students.append(new_student)

        for student in site.students:
            students_list = []
        for student in site.students:
            for course in student.courses:
                if course.name == course_name:
                    students_list.append(student)

        return '200 OK', render('new-student.html', objects_list=students_list, course_name=course_name)


@FrameRoute(routes_dict=routes_dict, url='/area-list/')
class AreaListView(ListView):
    query_set = site.areas
    template_name = 'area-list.html'


@FrameRoute(routes_dict=routes_dict, url='/area-creation/')
class AreaCreateView(CreateView):
    template_name = 'area-creation.html'

    """    def get_context_data(self):
        context = super().get_context_data()
        context[''] = site.courses
        context['students'] = site.students
        return context """

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        city = data['city']
        city = site.decode_value(city)
        address = data['address']
        address = site.decode_value(address)
        phone_number = data['phone_number']
        phone_number = site.decode_value(phone_number)

        new_obj = site.create_area(name, city, address, phone_number)
        site.areas.append(new_obj)


@FrameRoute(routes_dict=routes_dict, url='/api/')
class CourseApi:
    @FrameDebug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', PickleSerializer(site.courses).save()
