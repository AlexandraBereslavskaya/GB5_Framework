from simba_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from data.framework_data import SPECIALIST_DICT

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


class Schedule:
    def __call__(self, request):
        return '200 OK', render('schedule.html', data=request.get('data', None))


class Professionals:
    def __call__(self, request):
        return '200 OK', render('professionals.html', object_dict=SPECIALIST_DICT)


class About:
    def __call__(self, request):
        return '200 OK', 'The page is being finalized'


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class CoursesList:

    def __call__(self, request):
        logger.log('Список курсов')
        if 'id' in request['request_params']:
            print(int(request['request_params']['id']))
            category = site.find_category_by_id(int(request['request_params']['id']))
            print(category.courses)
            return '200 OK', render('course-list.html', objects_list=category.courses,
                                    name=category.name, category_id=category.category_id)
        else:
            try:
                courses_obj_list = site.get_all_courses()
                courses_list = []
                print(courses_obj_list)
                for course in courses_obj_list:
                    course_dict = {'course_name': course.name, 'course_category': course.category.name}
                    courses_list.append(course_dict)
                print(courses_list)

                return '200 OK', render('course-list.html', objects_list=courses_list)

            except KeyError:
                return '202 OK', 'No courses found'
        """       
        try:
            print(int(request['request_params']['id']))
            category = site.find_category_by_id(int(request['request_params']['id']))
            print(category.courses)
            return '200 OK', render('course-list.html', objects_list=category.courses,
                                    name=category.name, category_id=category.category_id)
        except KeyError:
            return '202 OK', 'No courses found'
        """

class CourseCreation:
    category_id = -1

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
                print(course.name)
                site.courses.append(course)

            return '200 OK', render('course-list.html', objects_list=category.courses,
                                    name=category.name, category_id=category.category_id)
        else:
            print("Get method")
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


class CourseCopy:

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


class CategoryCreation:

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


class CategoryList:

    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html', objects_list=site.categories)

"""
class ProfessionalCreation:

    def __call__(self, request):
        logger.log('Добавление специалиста')
        if request['method'] == 'POST':
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            speciality = data['speciality']
            speciality = site.decode_value(speciality)

            school = data['school']
            
            new_profession = site.create_user('professional')
            site.categories.append(new_category)

            return '200 OK', render('professionals.html', objects_list=site.professionals)
        else:
            return '200 OK', render('professional_creation.html', objects_list=site.professionals)
"""