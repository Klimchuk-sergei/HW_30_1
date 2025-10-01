from rest_framework.pagination import PageNumberPagination

class LessonPaginator(PageNumberPagination):
    page_size = 10 # кол-во уроков на странице
    page_size_query_param = 'page_size'
    max_page_size = 50

class CoursePaginator(PageNumberPagination):
    page_size = 5 # кол-во курсов на странице
    page_size_query_param = 'page_size'
    max_page_size = 20