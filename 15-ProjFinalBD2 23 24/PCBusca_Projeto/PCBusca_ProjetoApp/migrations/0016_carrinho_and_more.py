# Generated by Django 4.1.3 on 2024-02-04 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PCBusca_ProjetoApp', '0015_alter_stockcomponente_id_stock_and_more'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Carrinho',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('utilizador_id', models.IntegerField()),
        #         ('equipamento_id', models.IntegerField()),
        #         ('quantidade', models.IntegerField()),
        #     ],
        # ),
        migrations.RenameField(
            model_name='encomendacliente',
            old_name='equipamento',
            new_name='equipamento_id',
        ),
        migrations.RemoveField(
            model_name='encomendacomponente',
            name='encomenda',
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='data_encomenda_cliente',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='estado',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='id_encomenda_cliente',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='metodo_pagamento',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='morada_armazem',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='morada_cliente',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='nome_artigo',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='preco_enc_c',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='quantidade',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='encomendacliente',
            name='telemovel_cliente',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterUniqueTogether(
            name='encomendacliente',
            unique_together={('id_encomenda_cliente', 'equipamento_id')},
        ),
        migrations.AlterModelTable(
            name='encomendacliente',
            table='PCBusca_ProjetoApp_encomendacliente',
        ),
    ]
