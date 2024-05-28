import django_filters
from .models import Storage


class StorageListFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='actual_price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='actual_price', lookup_expr='lt')

    class Meta:
        model = Storage
        fields = (
            'cap__title',
            'cap__brands',
            'cap__cap_model',
            'cap__category',
            'status'
        )
