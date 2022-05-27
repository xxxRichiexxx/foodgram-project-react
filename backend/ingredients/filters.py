from rest_framework import filters
# from django.db.models import Q
from django.db.models import Case, Value, When, IntegerField


class IngredientsSearchFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            result = queryset.filter(name__icontains=name).annotate(
                Case(
                    When(name__istartswith=name, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            )
            # part_one = queryset.filter(name__istartswith=name)
            # part_two = queryset.filter(
            #     name__icontains=name
            # ).exclude(name__istartswith=name)
            # return part_one.union(part_two).order_by()[:50]
            # return part_one | part_two
            # return queryset.filter(
            #     Q(name__istartswith=name) | Q(name__icontains=name)
            # )[:50]
            return result.order_by('ordering_index', 'name')
        return queryset
