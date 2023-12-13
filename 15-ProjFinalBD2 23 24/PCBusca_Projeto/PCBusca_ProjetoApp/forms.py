from django.forms import ModelForm
from django import forms
from .models import Utilizador
from .models import Componente
from .models import Fornecedor
from .models import Equipamento
from .models import Funcionarios
from .models import MovimentacoesDeStock
from .models import Producao
from .models import StockComponente
from .models import TipoComponente, TipoDeEquipamento, TipoDeMaoDeObra

   

# class CreateUserForm(ModelForm):
#     class Meta:
#         model = Utilizadores
#         fields = ["nome","email","password", "NIF","telefone"]Utilizador
#         labels = {'nome': "Nome", 'email': "Email",'NIF': "NIF", 'telefone': "Telefone"}
        
# class AuthForm(ModelForm):
#     class Meta:
#         model = Utilizadores
#         fields = ["email", "password"]
#         labels = {'email': "Email", 'password': "password"}


from django import forms
from .models import Utilizador, Componente, EncomendaCliente, EncomendaComponente, Equipamento, FaturaCliente, Fornecedor, Funcionarios, GuiaDeRemessa, LinhaDeEncomenda, LinhaDeFatura, MovimentacoesDeStock, NotasDeEncomenda, Producao, Producao2, StockComponente, TipoDeEquipamento, TipoComponente, TipoDeMaoDeObra

class CreateUserForm(ModelForm):
    class Meta:
        model = Utilizador
        fields = ["nome","email","password", "NIF","telemovel","morada_utilizador"]
        labels = {'nome': "Nome", 'email': "Email",'NIF': "NIF", 'telemovel': "Telemovel",'morada_utilizador':"Morada"}
        
class AuthForm(ModelForm):
    class Meta:
        model = Utilizador
        fields = ["email", "password"]
        labels = {'email': "Email", 'password': "password"}
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Utilizador
        fields = ["nome","email","password", "NIF","telemovel"]
        labels = {'nome': "Nome", 'email': "Email",'NIF': "NIF", 'telemovel': "Telemovel"}
        exclude = ['id_cliente', 'id_fatura_cliente', 'id_encomenda_cliente']

class UtilizadorForm(ModelForm):
    class Meta:
        model=Utilizador
        fields = ["nome","email","password", "NIF","telemovel"]
        labels = {'nome': "Nome", 'email': "Email",'NIF': "NIF", 'telemovel': "Telemovel"}
        #exclude = ['id_cliente', 'id_fatura_cliente', 'id_encomenda_cliente']

class UtilizadorForm2(ModelForm):
    class Meta:
        model=Utilizador
        fields = ["nome","morada_utilizador","email", "NIF","telemovel"]
        labels = {'nome': "Nome",'morada_utilizador': "Morada_utilizador", 'email': "Email",'NIF': "NIF", 'telemovel': "Telemovel"}
        #exclude = ['id_cliente', 'id_fatura_cliente', 'id_encomenda_cliente']


class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Componente
        exclude = ['id_componente', 'id_fornecedor', 'id_tipo_componente']


class EncomendaClienteForm(forms.ModelForm):
    class Meta:
        model = EncomendaCliente
        exclude = ['id_encomenda_cliente', 'id_cliente', 'id_equipamento']


class EncomendaComponenteForm(forms.ModelForm):
    class Meta:
        model = EncomendaComponente
        exclude = ['id_encomenda_componente', 'id_encomenda', 'id_componente']


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        exclude = ['id_equipamento', 'id_tipo_de_equipamento', 'id_componente', 'id_producao']


class FaturaClienteForm(forms.ModelForm):
    class Meta:
        model = FaturaCliente
        exclude = ['id_fatura_cliente', 'id_encomenda_cliente']


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        exclude = ['id_fornecedor']


class FuncionariosForm(forms.ModelForm):
    class Meta:
        model = Funcionarios
        exclude = ['id_funcionario']


class GuiaDeRemessaForm(forms.ModelForm):
    class Meta:
        model = GuiaDeRemessa
        exclude = ['id_guia_de_remessa', 'id_encomenda']


class LinhaDeEncomendaForm(forms.ModelForm):
    class Meta:
        model = LinhaDeEncomenda
        exclude = ['id_linha_de_encomenda', 'id_encomenda_cliente']


class LinhaDeFaturaForm(forms.ModelForm):
    class Meta:
        model = LinhaDeFatura
        exclude = ['id_linha_de_fatura', 'id_fatura_cliente', 'id_equipamento']


class MovimentacoesDeStockForm(forms.ModelForm):
    class Meta:
        model = MovimentacoesDeStock
        exclude = ['id_movimentacao_stock', 'id_producao', 'id_fatura_cliente', 'id_guia_de_remessa']


class NotasDeEncomendaForm(forms.ModelForm):
    class Meta:
        model = NotasDeEncomenda
        exclude = ['id_encomenda', 'id_guia_de_remessa']


class ProducaoForm(forms.ModelForm):
    class Meta:
        model = Producao
        exclude = ['id_producao']


class Producao2Form(forms.ModelForm):
    class Meta:
        model = Producao2
        exclude = ['id_equipamento', 'id_componente']


class StockComponenteForm(forms.ModelForm):
    class Meta:
        model = StockComponente
        exclude = ['id_stock']


class TipoDeEquipamentoForm(forms.ModelForm):
    class Meta:
        model = TipoDeEquipamento
        exclude = ['id_tipo_de_equipamento']


class TipoComponenteForm(forms.ModelForm):
    class Meta:
        model = TipoComponente
        exclude = ['id_tipo_componente']


class TipoDeMaoDeObraForm(forms.ModelForm):
    class Meta:
        model = TipoDeMaoDeObra
        exclude = ['id_tipo_mao_de_obra', 'id_funcionario']

