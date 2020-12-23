from rest_framework import pagination


class SmallResultsSetPagination(pagination.PageNumberPagination):
    page_size = 3
