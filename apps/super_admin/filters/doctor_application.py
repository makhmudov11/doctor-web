import django_filters

from apps.doctor_application.models import DoctorApplication


class AdminDoctorApplicationListFilter(django_filters.FilterSet):
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_at__gte = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_at__lte = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = DoctorApplication
        fields = ['created_at__gte', 'created_at__lte', 'updated_at__gte', 'updated_at__lte']