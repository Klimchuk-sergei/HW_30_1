from rest_framework.pagination import PageNumberPagination


class LessonPaginator(PageNumberPagination):
    page_size = 10  # Количество уроков на странице
    page_size_query_param = 'page_size'
    max_page_size = 50