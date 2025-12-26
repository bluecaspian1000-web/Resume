# courses/filters.py
import django_filters as filters
from .models import CourseOffering
from django.db.models import Q

class CourseOfferingFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_by_all')
    """
    course_code = filters.CharFilter(
        field_name='course__code',
        lookup_expr='icontains'
    )

    course_name = filters.CharFilter(
        field_name='course__name',
        lookup_expr='icontains'
    )

    prof_name = filters.CharFilter(
        field_name='prof_name',
        lookup_expr='icontains'
    )

    

    min_capacity = filters.NumberFilter(
        field_name='capacity',
        lookup_expr='gte'
    )

    session_day = filters.CharFilter(
        field_name='sessions__day',
        lookup_expr='exact'
    )
    """

    class Meta:
        model = CourseOffering
        fields = []
    
    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(course__name__icontains=value) |
            Q(course__code__icontains=value) |
            Q(prof__name__icontains=value)
        )
    