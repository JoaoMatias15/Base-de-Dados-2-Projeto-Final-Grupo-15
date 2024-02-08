from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.registerPage, name='registerPage'),
    path('login', views.login_view, name='login'),
    path('admin', views.bomdia_admin, name='bomdia_admin'),
    path('admin/listar_utilizadores/', views.listar_utilizadores, name='listar_utilizadores'),
    path('admin/criar_utilizadores/', views.criar_utilizador, name='criar_utilizador'),
    path('admin/editar/<int:id>/', views.update_utilizador, name='editar_utilizador'),
    path('admin/trocar_estado_utilizador/<int:id>/', views.trocarEstado, name='trocar_estado_utilizador'),
    path('admin/listar_fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    path('admin/inserir_forn/', views.inserir_forn, name='inserir_forn'),
    path('admin/editar_fornecedor/<int:id>/', views.editar_fornecedores, name='editar_fornecedor'),
    path('admin/apagar_fornecedor/<int:id>/', views.apagar_fornecedores, name='apagar_fornecedor'),
    path('admin/inserir_componente/', views.insert_componente, name='inserir_componente'),
    path('admin/listar_componentes/', views.get_componentes, name='listar_componentes'),
    path('admin/editar_componente/<int:id>/', views.update_componente, name='editar_componente'),
    path('admin/apagar_componente/<int:id>/', views.apagar_componente, name='apagar_componente'),
    path('admin/inserir_equipamento/', views.insert_equipamento, name='inserir_equipamento'),
    path('admin/listar_equipamentos/', views.get_equipamentos, name='listar_equipamentos'),
    path('admin/editar_equipamento/<int:id>/', views.update_equipamento, name='editar_equipamento'),
    path('admin/apagar_equipamento/<int:id>/', views.apagar_equipamento, name='apagar_equipamento'),
    path('admin/listar_tipo_componentes/', views.get_tipo_componentes, name='listar_tipo_componentes'),
    path('admin/inserir_tipo_componente/', views.insert_into_tipo_componentes, name='inserir_tipo_componente'),
    path('admin/editar_tipo_componente/<int:id>/', views.update_tipo_componente, name='editar_tipo_componente'),
    path('admin/apagar_tipo_componente/<int:id>/', views.apagar_tipo_componente, name='apagar_tipo_componente'),
    path('admin/listar_tipo_equipamentos/', views.get_tipo_equipamentos, name='listar_tipo_equipamentos'),
    path('admin/inserir_tipo_equipamento/', views.insert_tipo_equipamento, name='inserir_tipo_equipamento'),
    path('admin/editar_tipo_equipamento/<int:id>/', views.update_tipo_equipamento, name='editar_tipo_equipamento'),
    path('admin/apagar_tipo_equipamento/<int:id>/', views.apagar_tipo_equipamento, name='apagar_tipo_equipamento'),
    path('admin/listar_tipo_mao_de_obra/', views.get_tipo_mao_de_obra, name='listar_tipo_mao_de_obra'),
    path('admin/inserir_tipo_mao_de_obra/', views.inserir_tipo_mao_de_obra, name='inserir_tipo_mao_de_obra'),
    path('admin/editar_tipo_mao_de_obra/<int:id>/', views.update_tipo_mao_de_obra, name='editar_tipo_mao_de_obra'),
    path('admin/apagar_tipo_mao_de_obra/<int:id>/', views.apagar_tipo_mao_de_obra, name='apagar_tipo_mao_de_obra'),
    path('admin/listar_producoes/', views.get_producoes, name='listar_producoes'),
    path('admin/inserir_producao', views.insert_producao, name='inserir_producao'),
    path('admin/editar_producao/<int:id>/', views.update_producao, name='editar_producao'),
    path('admin/apagar_producao/<int:id>/', views.apagar_producao, name='apagar_producao'),
    path('carrinho', views.carrinho, name='carrinho'),
    path('finalizar_compra', views.create_encomenda, name='finalizar_compra'),
    path('adicionar_ao_carrinho/<int:p_equipamento_id>', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/<int:p_equipamento_id>', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('apanhar_carrinho', views.limpar_carrinho, name='apanhar_carrinho'),
    path('admin/listar_tipo_utilizador/', views.get_tipo_utilizador, name='listar_tipo_utilizador'),
    path('admin/inserir_tipo_utilizador/', views.inserir_tipo_utilizador, name='inserir_tipo_utilizador'),
    path('admin/editar_tipo_utilizador/<int:id>/', views.update_tipo_utilizador, name='editar_tipo_utilizador'),
    path('admin/apagar_tipo_utilizador/<int:id>/', views.apagar_tipo_utilizador, name='apagar_tipo_utilizador'),
    path('admin/listar_funcionario/', views.get_funcionario, name='listar_funcionario'),
    path('admin/inserir_funcionario/', views.insert_funcionario, name='inserir_funcionario'),
    path('admin/editar_funcionario/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('admin/apagar_funcionario/<int:id>/', views.apagar_funcionario, name='apagar_funcionario'),
    path('minhasencomendas', views.get_encomendas, name='minhasencomendas'),
    path('admin/insert_bulk_componente/', views.insert_bulk_componente, name='insert_bulk_componente'),
    path('admin/listar_guia_de_remessa/', views.get_guias, name='listar_guia_de_remessa'),
    path('admin/apagar_guia_de_remessa/<int:id>/', views.apagar_guia, name='apagar_guia_de_remessa'),
    path('admin/inserir_guia_de_remessa/', views.insert_guia_de_remessa, name='inserir_guia_de_remessa'),
    path('admin/guiaderemessa/', views.guiaderemessa_list, name='guiaderemessa_list'),
    path('admin/listar_encomendascliente', views.list_encomenda_cliente, name='listar_encomendascliente'),
    path('admin/editar_encomendacliente/<int:id>/', views.edit_encomenda_cliente, name='editar_encomendacliente'),
    path('admin/apagar_encomendacliente/<int:id>/', views.delete_encomenda_cliente, name='apagar_encomendacliente'),
    path('listar_fatura/', views.listar_faturas_cliente, name='listar_fatura'),
    path('logout/', views.logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
