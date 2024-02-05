import django_filters

from .models import *

class EquipamentoFilter(django_filters.FilterSet):
    precoMax = django_filters.NumberFilter(field_name='preco', lookup_expr='lte', label= 'Preço Máximo')
    nome = django_filters.CharFilter(field_name='nome', lookup_expr='icontains')
    class Meta:
        model = Equipamento
        fields = ['tipo_equipamento']