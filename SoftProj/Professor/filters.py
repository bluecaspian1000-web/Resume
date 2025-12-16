# filters.py
import django_filters
from .models import Professor

class ProfessorFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    professor_code = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Professor
        fields = ['username', 'first_name', 'last_name', 'professor_code']
