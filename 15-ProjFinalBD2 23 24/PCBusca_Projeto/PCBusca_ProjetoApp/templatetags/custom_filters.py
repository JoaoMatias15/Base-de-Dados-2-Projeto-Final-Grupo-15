from django import template
from django.db import connections
from PCBusca_ProjetoApp.models import Fornecedor,TipoComponente

register = template.Library()

@register.filter(name='get_fornecedor_name')
def get_fornecedor_name(fornecedor_id):
    try:
        with connections['postgres'].cursor() as cursor:
            cursor.callproc('get_fornecedor_by_id', [fornecedor_id])
            forn = cursor.fetchone()
            print('--------------------------------------------------------------------------------------------------------------------')
            print(forn)
            print('--------------------------------------------------------------------------------------------------------------------')
            if forn:
                return forn[1]
            else:
                return 'Fornecedor not found'
    except Fornecedor.DoesNotExist:
        return 'Fornecedor not found'

@register.filter(name='get_tipo_componente_name')
def get_tipo_componente_name(tipo_componente_id):
    try:
        with connections['postgres'].cursor() as cursor:
            cursor.callproc('get_tipo_componente_by_id', [tipo_componente_id])
            tipo_componente = cursor.fetchone()
            print('--------------------------------------------------------------------------------------------------------------------')
            print(tipo_componente)
            print('--------------------------------------------------------------------------------------------------------------------')
            if tipo_componente:
                return tipo_componente[1]  # Adjust the index if the name is in a different position
            else:
                return 'Tipo Componente not found'
    except TipoComponente.DoesNotExist:
        return 'Tipo Componente not found'