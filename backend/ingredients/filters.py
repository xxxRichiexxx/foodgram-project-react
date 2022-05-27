from rest_framework import filters


class IngredientsSearchFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            part_one = queryset.filter(name__istartswith=name)
            part_two = queryset.filter(name__icontains=name)
            return part_two.union(part_one)[:50]
        return queryset
