from django.db import models

class TipoUtilizador(models.Model):
    id_tipo_utilizador = models.AutoField(primary_key=True)
    tipo_utilizador = models.CharField(max_length=256, null=True)
    

class Utilizador(models.Model):
    id_utilizador = models.AutoField(primary_key=True)
    #TODO:Verificar os models por causa das FKs de Fatura e Encomendas
    #fatura_utilizador = models.ForeignKey('FaturaCliente', on_delete=models.SET_NULL, null=True)
    #encomenda_utilizador = models.ForeignKey('EncomendaCliente', on_delete=models.SET_NULL, null=True)
    tipo_utilizador = models.ForeignKey('TipoUtilizador', on_delete=models.SET_NULL, null=True)
    morada_utilizador = models.CharField(max_length=256, null=True)
    nome = models.CharField(max_length=256, null=True)
    email = models.CharField(max_length=256, null=True)
    telemovel = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    NIF = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    estado = models.BooleanField(null=True)
    data_desativado = models.DateTimeField(null=True)
    password = models.CharField(max_length=256, null=True)   

class Componente(models.Model):
    id_componente = models.AutoField(primary_key=True)
    fornecedor = models.ForeignKey('Fornecedor', on_delete=models.SET_NULL, null=True)
    tipo_componente = models.ForeignKey('TipoComponente', on_delete=models.SET_NULL, null=True)
    nome_componente = models.CharField(max_length=256)
    stock = models.IntegerField()
    preco_compra = models.FloatField(null=True)
    peso = models.FloatField(null=True)
    caracteristicas = models.CharField(max_length=256, null=True)
    margem_lucro = models.FloatField(null=True)
    stock_min = models.IntegerField(null=True)

class EncomendaCliente(models.Model):
    id_encomenda_cliente = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Utilizador', on_delete=models.SET_NULL, null=True)
    equipamento = models.ForeignKey('Equipamento', on_delete=models.SET_NULL, null=True)
    preco_enc_c = models.FloatField(null=True)
    morada_armazem = models.CharField(max_length=256, null=True)
    morada_cliente = models.CharField(max_length=256, null=True)
    quantidade = models.IntegerField(null=True)
    data_encomenda_cliente = models.DateTimeField(null=True)
    nome_artigo = models.CharField(max_length=256, null=True)
    telemovel_cliente = models.CharField(max_length=256, null=True)
    metodo_pagamento = models.CharField(max_length=256, null=True)
    estado = models.CharField(max_length=256, null=True)

class EncomendaComponente(models.Model):
    id_encomenda_componente = models.AutoField(primary_key=True)
    encomenda = models.ForeignKey('EncomendaCliente', on_delete=models.SET_NULL, null=True)
    componente = models.ForeignKey('Componente', on_delete=models.SET_NULL, null=True)

class Equipamento(models.Model):
    id_equipamento = models.AutoField(primary_key=True)
    tipo_equipamento = models.ForeignKey('TipoDeEquipamento', on_delete=models.SET_NULL, null=True)
    componente = models.ForeignKey('Componente', on_delete=models.SET_NULL, null=True)
    producao = models.ForeignKey('Producao', on_delete=models.SET_NULL, null=True, related_name='equipamentos')
    # producao = models.ForeignKey('Producao', on_delete=models.SET_NULL, null=True)
    preco_equipamento = models.FloatField()
    preco_de_producao = models.FloatField()
    stock_equip = models.IntegerField()
    caracteristicas_equip = models.CharField(max_length=256, null=True)
    margem_lucro_equip = models.IntegerField(null=True)
    stock_min_equip = models.CharField(max_length=10, null=True)
    
    

class FaturaCliente(models.Model):
    #TODO: Adicionar id utilizador(Secalhar nem e necessario pois podemos obter o utilizador atraves da Encomenda!!)
    id_fatura_cliente = models.AutoField(primary_key=True)
    encomenda_cliente = models.ForeignKey('EncomendaCliente', on_delete=models.SET_NULL, null=True)
    nif_loja = models.IntegerField(null=True)
    nome_cliente = models.CharField(max_length=256, null=True)
    nome_loja = models.CharField(max_length=256, null=True)
    artigo = models.CharField(max_length=256, null=True)
    quantidade = models.IntegerField(null=True)
    preco_total = models.FloatField(null=True)
    data_emissao_fatura = models.DateTimeField(null=True)

class Fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome_fornecedor = models.CharField(max_length=256, null=True)
    morada_fornecedor = models.CharField(max_length=256, null=True)
    email_fornecedor = models.CharField(max_length=256, null=True)
    telemovel_fornecedor = models.IntegerField(null=True)
    nif = models.IntegerField(null=True)

class Funcionarios(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome_funcionario = models.CharField(max_length=256, null=True)
    morada_funcionario = models.CharField(max_length=256, null=True)
    telemovel_funcionario = models.IntegerField(null=True)
    idade = models.IntegerField(null=True)

class GuiaDeRemessa(models.Model):
    id_guia_de_remessa = models.AutoField(primary_key=True)
    encomenda = models.ForeignKey('EncomendaCliente', on_delete=models.SET_NULL, null=True)
    fornecedor = models.ForeignKey('Fornecedor', on_delete=models.SET_NULL, null=True)
    destinatario = models.CharField(max_length=256, null=True)
    nif_destinatario = models.IntegerField(null=True)
    data_saida_forn = models.DateTimeField(null=True)
    nome_produto = models.CharField(max_length=256, null=True)
    quantidade_produto = models.IntegerField(null=True)
    peso_produto = models.FloatField(null=True)

class LinhaDeEncomenda(models.Model):
    id_linha_de_encomenda = models.AutoField(primary_key=True)
    encomenda_cliente = models.ForeignKey('EncomendaCliente', on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=256, null=True)
    designacao_de_artigo = models.CharField(max_length=256, null=True)
    preco_unitario = models.FloatField(null=True)
    quantidade_encomendada = models.IntegerField(null=True)
    preco_total = models.FloatField(null=True)

class LinhaDeFatura(models.Model):
    id_linha_de_fatura = models.AutoField(primary_key=True)
    fatura_cliente = models.ForeignKey('FaturaCliente', on_delete=models.SET_NULL, null=True)
    equipamento = models.ForeignKey('Equipamento', on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=256, null=True)
    designacao_de_artigo = models.CharField(max_length=256, null=True)
    preco_unitario = models.FloatField(null=True)
    quantidade = models.IntegerField(null=True)
    preco_total = models.FloatField(null=True)

class MovimentacoesDeStock(models.Model):
    id_movimentacao_stock = models.AutoField(primary_key=True)
    producao = models.ForeignKey('Producao', on_delete=models.SET_NULL, null=True)
    fatura_cliente = models.ForeignKey('FaturaCliente', on_delete=models.SET_NULL, null=True)
    guia_de_remessa = models.ForeignKey('GuiaDeRemessa', on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField(null=True)

class NotasDeEncomenda(models.Model):
    encomenda = models.IntegerField(primary_key=True)
    guia_de_remessa = models.ForeignKey('GuiaDeRemessa', on_delete=models.SET_NULL, null=True)
    nome_encomenda = models.CharField(max_length=256, null=True)
    morada_fornecedor = models.CharField(max_length=256, null=True)
    valor_total = models.FloatField(null=True)
    data_de_envio = models.DateTimeField(null=True)
    data_de_chegada = models.DateTimeField(null=True)

class Producao(models.Model):
    id_producao = models.AutoField(primary_key=True)
    componente = models.ForeignKey('Componente', on_delete=models.SET_NULL, null=True)
    # equipamento = models.ForeignKey('Equipamento', on_delete=models.SET_NULL, null=True)
    equipamento = models.ForeignKey('Equipamento', on_delete=models.SET_NULL, null=True, related_name='producoes')
    tipo_mao_de_obra = models.ForeignKey('TipoDeMaoDeObra', on_delete=models.SET_NULL, null=True)
    horas_producao = models.FloatField(null=True)
    custos = models.FloatField(null=True)

# class Producao2(models.Model):
#     equipamento = models.OneToOneField('Equipamento', on_delete=models.CASCADE, primary_key=True)
#     componente = models.OneToOneField('Componente', on_delete=models.CASCADE, primary_key=True)

class Producao2(models.Model):
    equipamento = models.ForeignKey('Equipamento', on_delete=models.CASCADE)
    componente = models.ForeignKey('Componente', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('equipamento', 'componente')

class StockComponente(models.Model):
    id_stock = models.CharField(primary_key=True, max_length=10)
    quantidade = models.IntegerField(null=True)
    preco_stock = models.CharField(max_length=10, null=True)

class TipoDeEquipamento(models.Model):
    id_tipo_de_equipamento = models.IntegerField(primary_key=True)
    designacao_tipo_de_equipamento = models.CharField(max_length=256, null=True)

class TipoComponente(models.Model):
    id_tipo_componente = models.IntegerField(primary_key=True)
    designacao_tipo_componente = models.CharField(max_length=256, null=True)

class TipoDeMaoDeObra(models.Model):
    id_tipo_mao_de_obra = models.IntegerField(primary_key=True)
    funcionario = models.ForeignKey('Funcionarios', on_delete=models.SET_NULL, null=True)
    descricao_tipo_mao_de_obra = models.CharField(max_length=256, null=True)


# models_mongodb.py
from djongo import models

class MongoModel(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        # especifica o banco de dados
        app_label = 'mongodb'
