from reviews.models import Title
from django_filters import rest_framework as filters

class TitlesFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact',
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact',
    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )
    year = filters.NumberFilter(
        field_name='year',
        lookup_expr='icontains',
    )

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
