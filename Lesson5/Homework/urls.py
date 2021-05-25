from datetime import date
"""
from views import Index, Professionals, About, CoursesList, CourseCreation, CourseCopy, CategoryCreation, CategoryList, \
    Schedule
"""


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

"""routes = {
    '/': Index(),
    '/index/': Index(),
    '/schedule/': Schedule(),
    '/professionals/': Professionals(),
    '/course-list/': CoursesList(),
    '/course-creation/': CourseCreation(),
    '/course-copy/': CourseCopy(),
    '/category-list/': CategoryList(),
    '/category-creation/': CategoryCreation(),
    '/about/': About()
}
"""

