from rest_framework import filters
from django.db.models import Case, Value, When, IntegerField


class IngredientsSearchFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            result = queryset.filter(name__icontains=name).annotate(
                ordering_index=Case(
                    When(name__istartswith=name, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            )
            return result.order_by('ordering_index', 'name')
        return queryset
