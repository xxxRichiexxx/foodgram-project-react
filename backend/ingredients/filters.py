from rest_framework import filters
# from django.db.models import Q


class IngredientsSearchFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            part_one = queryset.filter(name__istartswith=name)
            part_two = queryset.filter(
                name__icontains=name
            ).exclude(name__istartswith=name)
            return part_one.union(part_two).order_by()[:50]
            # return queryset.filter(
            #     Q(name__istartswith=name) | Q(name__icontains=name)
            # )[:50]
        return queryset
