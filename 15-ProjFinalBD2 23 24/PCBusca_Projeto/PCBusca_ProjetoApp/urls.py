from django.urls import path
from . import views



urlpatterns =[
    path('',views.index,name= 'index'),
    path('register',views.registerPage,name='registerPage'),
    #path('test_insert',views.view_insert_user,name='test_insert'),
    path('login',views.login_view,name='login'),
    path('admin/listar_utilizadores/', views.listar_utilizadores, name='listar_utilizadores'),
    # path('admin', views.bomdia_admin, name='bomdia_admin'),
    # path('cart', views.cart, name='cart'),
    path('admin', views.bomdia_admin, name='bomdia_admin'),
    path('admin/listar_utilizadores/', views.listar_utilizadores, name='listar_utilizadores'),
    path('admin/criar_utilizadores/', views.criar_utilizador, name='criar_utilizador'),
    path('admin/editar/<int:id>/', views.editar_utilizador, name='editar_utilizador'),
    #path('admin/apagar/<int:id>/', views.apagar_utilizador, name='apagar_utilizador'),
    path('admin/trocar_estado_utilizador/<int:id>/', views.trocarEstado,name='trocar_estado_utilizador'),
    #TODO:
    path('admin/listar_fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    #path('admin/criar_fornecedores/', views.criar_fornecedores, name='criar_fornecedores'),#needs html
    #path('admin/editar_fornecedores/<int:id>/', views.editar_fornecedores, name='editar_fornecedores'),#needs html
    #path('admin/apagar_fornecedores/<int:id>/', views.apagar_fornecedores, name='apagar_fornecedores'),
]