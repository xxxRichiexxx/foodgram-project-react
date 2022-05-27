from rest_framework import filters
from django.db.models import Q


class IngredientsSearchFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            return queryset.filter(Q(name__istartswith=name)|Q(name__icontains=name))[:50]
        return queryset
