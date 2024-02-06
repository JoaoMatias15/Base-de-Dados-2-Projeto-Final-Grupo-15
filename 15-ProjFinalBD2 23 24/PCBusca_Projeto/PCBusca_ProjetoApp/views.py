from django.shortcuts import render
from django.db import connections
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.shortcuts import redirect
from django.forms import ModelForm
from .models import Carrinho, EncomendaCliente
from django.db import transaction
from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .filters import EquipamentoFilter
from .forms import CreateUserForm,AuthForm,UtilizadorForm,UtilizadorForm2,FornecedorForm,ComponenteForm
from .models import Utilizador
from .models import Equipamento
from django.conf import settings

# from .models import Produtos
# from .filters import ProdutosFilter
# from .forms import UtilizadorForm
# from .forms import ProdutosForm
# from .models import Fornecedores
# from .forms import FornecedoresForm
from django.db import connections
from django.shortcuts import render,get_object_or_404, redirect
from .models import Carrinho
	

def registerPage(request):
    context = {}
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email_Form = form.cleaned_data['email']
            #TODO:  Verificar se utilizador existe(Nota: Usar uma função de check email e dar throw (ver login))!!!!!!!!!!!!!!
            #if Utilizador.objects.filter(email=email_Form).exists():
                #form.add_error('email', 'Já tens conta!')
                #return render(request, 'auth/register.html', context)
            # utilizador = form.save(commit=False)
            # utilizador.nome = form.cleaned_data['nome']
            # utilizador.email = email_Form
            # utilizador.password = make_password(form.cleaned_data['password'])
            # utilizador.NIF = form.cleaned_data['NIF'] 
            # utilizador.telemovel = form.cleaned_data['telemovel'] 
            #utilizador.tipoCliente = 'Cliente'
            # Get the database connection
            with connections['postgres'].cursor() as cursor:
                try:
                    cursor.callproc('check_email_exists', [
                    email_Form
                ])
                except Exception as e:
                    messages.warning(request, 'Email ja utilizado numa conta!')	
                    return render(request, 'auth/register.html', context)
                # Call the PostgreSQL function
                cursor.callproc('insert_into_utilizador', [
                    form.cleaned_data['morada_utilizador'], form.cleaned_data['nome'], email_Form, form.cleaned_data['telemovel'] , form.cleaned_data['NIF'], None,make_password(form.cleaned_data['password'],'Bd2'),  # Pass your function arguments here
                ])
                
                # If your function returns something, fetch the result
                result = cursor.fetchall()
            # Process the result or perform further actions
            # ...
            # Return an HTTP response or render a template
            print(result)
            #return render(request, 'auth/register.html')
            #form.save()
            return redirect('index')
    return render(request, 'auth/register.html', context)

def login_view(request):
    context = {}
    if request.method == 'POST':
        form = AuthForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print("Tou Valido")
            email_form = form.cleaned_data['email']
            with connections['postgres'].cursor() as cursor:
                cursor.callproc('user_login', [
                        form.cleaned_data['email'], make_password(form.cleaned_data['password'],'Bd2'), 
                    ])
                try:print()
                    
                    
                except Exception as e:
                    print('--------------------------------------------------------------------------------------------------------------------------')
                    print('Error do Postgres ao Login')
                    print("Error:", str(e))
                    print('--------------------------------------------------------------------------------------------------------------------------')
                    messages.warning(request, 'Erro no login')
                    # Handle case where user does not exist
                    pass
                userid = cursor.fetchall()
                response = redirect('index')
                response.set_cookie("loginToken", userid)
                return response
        else:
            messages.error(request, 'Invalid email or password')
    else:
        
        form = AuthForm()
    return render(request, 'auth/login.html', context)

def index(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamentos_data_users')
        equipamentos = cursor.fetchall()
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(equipamentos)
        print('--------------------------------------------------------------------------------------------------------------------------')
    return render(request, 'cliente/mainmenu.html', {'equipamentos': equipamentos,})

# def cart(request):
#     # Get the cart from the cookies
#     cart = json.loads(request.COOKIES.get('cart')) or {}

#     print('--------------------------------------------------------------------------------------------------------------------------')
#     print(cart)
#     print('--------------------------------------------------------------------------------------------------------------------------')

#     # Get the product IDs from the cart
#     product_ids = list(cart.keys())
#     print('--------------------------------------------------------------------------------------------------------------------------')
#     print(product_ids)
#     print('--------------------------------------------------------------------------------------------------------------------------')

#     # Retrieve the products from the MongoDB database using Djongo
#     products = Produtos.objects.filter(id__in=product_ids)
#     print('--------------------------------------------------------------------------------------------------------------------------')
#     print(products)
#     print('--------------------------------------------------------------------------------------------------------------------------')
#     if request.method == 'POST':
#         cart = json.loads(request.COOKIES.get('cart')) or {}
#         product_ids = list(cart.keys())
#         products = Produtos.objects.filter(id__in=product_ids)
#         precoTotalEncomenda = 0
#         for product in products:
#             precoTotalEncomenda += product.preco
#             print('--------------------------------------------------------------------------------------------------------------------------')
#             print('Teste de preco total da encomenda')
#             print(precoTotalEncomenda)
#             stockCheck = product.stock - cart[str(product.id)]#atualizar stock
#             if stockCheck < 0:
#                 messages.warning(request, 'O stock do produto ' + product.nome + 'não é suficiente para a encomenda')
#                 return redirect('cart')
#             #atualizar stock
#             product.stock = stockCheck
#             product.save()  
#         id_Utilizador = request.COOKIES.get('loginToken')
#         if id_Utilizador is None:
#             messages.warning(request, 'Não tens sessão iniciada')
#             return render(request, 'cliente/cart.html', {'products': products, 'cart': cart})
#         #inserir encomenda
#         with connections['postgres'].cursor() as cursor:
#             try:
#                 cursor.execute("SELECT insert_encomenda_function(%s, %s);", (id_Utilizador, precoTotalEncomenda))
#                 result = cursor.fetchone()
#             except Exception as e:
#                 print('--------------------------------------------------------------------------------------------------------------------------')
#                 print('Error do Postgres ao inserir encomenda')
#                 print("Error:", str(e))
#                 print('--------------------------------------------------------------------------------------------------------------------------')
#                 messages.warning(request, 'Erro ao inserir encomenda')
#                 return render(request, 'cliente/cart.html', {'products': products, 'cart': cart})
#         #inserir produtos encomenda
#         for product in products:
#             with connections['postgres'].cursor() as cursor:
#                 try:
#                     cursor.execute("call insert_artigo_encomenda(%s, %s, %s,%s);", (result[0],product.id,cart[str(product.id)], product.preco))
#                 except Exception as e:
#                     print('--------------------------------------------------------------------------------------------------------------------------')
#                     print('Error do Postgres ao inserir produtos encomenda')
#                     print("Error:", str(e))
#                     print('--------------------------------------------------------------------------------------------------------------------------')
#                     messages.warning(request, 'Erro ao inserir produtos encomenda')
#                     return render(request, 'cliente/cart.html', {'products': products, 'cart': cart})
#         #limpar carrinho
#         response = redirect('index')
#         response.delete_cookie('cart') 
#         return response#página de sucesso de encomenda
#     # Pass the products and cart quantities to the template
#     return render(request, 'cliente/cart.html', {'products': products, 'cart': cart})

def bomdia_admin(request):
    context = {}
    return render(request,'admin/bomdia_admin.html',context)

#Gerir Utilizadores 
def listar_utilizadores(request):
    with connections['postgres'].cursor() as cursor:       
        cursor.callproc('get_users_data')
        utilizadores = cursor.fetchall()
    context = {'utilizadores': utilizadores}
    print('--------------------------------------------------------------------------------------------------------------------------')
    print(utilizadores)
    print('--------------------------------------------------------------------------------------------------------------------------')
    return render(request, 'admin/listar_utilizadores.html', context)

# def criar_utilizador(request):
#     form = UtilizadorForm(request.POST or None)
#     print(form.errors)
#     if form.is_valid():
#         form.save()
#         return redirect('listar_utilizadores')
#     return render(request, 'admin/criar_utilizador.html', {'form': form})

def criar_utilizador(request):
    if request.method == 'POST':
        # Get form data
        nome = request.POST['nome']
        morada = request.POST['morada_utilizador']
        email = request.POST['email']
        telemovel = request.POST['telefone']
        nif = request.POST['NIF']
        tipo_utilizador_id = request.POST['tipo_utilizador_id']
        password = request.POST['password']
        print('--------------------------------------------------------------------------------------------------------------------------')
        print('%s,%s,%s,%s,%s,%s' % (nome, morada, email, telemovel, nif, tipo_utilizador_id))
        print('--------------------------------------------------------------------------------------------------------------------------')
        # Call procedure to insert into 'utilizadores'
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            Select * from insert_into_utilizador_admin(
                %s::varchar, %s::varchar, %s::varchar, %s::numeric,
                %s::numeric, %s::integer,%s::varchar
            )""",
            [morada, nome, email, telemovel, nif, tipo_utilizador_id, make_password(password,'Bd2')])

        return redirect('listar_utilizadores')
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipos_utilizadores_data')
        tipo_utilizadores = cursor.fetchall()
    return render(request, 'admin/criar_utilizador.html', {'tipo_utilizadores': tipo_utilizadores})


    

# def editar_utilizador(request, id):
#     with connections['postgres'].cursor() as cursor:
#         cursor.callproc('get_user_by_id', [
#             id
#         ])
#         user = cursor.fetchall()
#     #TODO: Meter no editUtilizador.html aquilo a preencher os campos com os dados da base de dados
#     form = UtilizadorForm(request.POST )
#     if request.method == 'POST':
#         cursor.callproc('update_user', [
#             id, form.cleaned_data['morada_utilizador'],form.cleaned_data['nome'], form.cleaned_data['email'], form.cleaned_data['telefone'], form.cleaned_data['NIF'] , None
#         ])
#     return render(request, 'admin/editar_utilizador.html', {'user': user})

# def editar_utilizador(request, id):
#     with connections['postgres'].cursor() as cursor:
#         cursor.callproc('get_user_by_id', [
#             id
#         ])
#         user = cursor.fetchone()
#     #TODO: Meter isto a editar, nao esta a enviar os dados para a base de dados
#     print(user)
#     form = UtilizadorForm2(request.POST, initial={
#             'nome': user[2],
#             'morada_utilizador': user[1],
#             'email': user[3],
#             'NIF': user[5],
#             'telemovel': user[4],
#         })
#     if request.method == 'POST':
#         print('--------------------------------------------------------------------------------------------------------------------------')
#         print(form.errors)
#         print('--------------------------------------------------------------------------------------------------------------------------')
#         if form.is_valid():
#             with connections['postgres'].cursor() as cursor:
#                 cursor.execute("CALL update_user(%s, %s, %s, %s, %s, %s)",
#                                [id, form.cleaned_data['morada_utilizador'],
#                                 form.cleaned_data['nome'],
#                                 form.cleaned_data['email'],
#                                 form.cleaned_data['telemovel'],
#                                 form.cleaned_data['NIF']
#                                 ])
                
#             return redirect('listar_utilizadores')    
#     return render(request, 'admin/editar_utilizador.html', {'user': user})


def update_utilizador(request, id):
    # Get 'utilizador' data by ID
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_user_by_id', [id])
        utilizador = cursor.fetchone()

    # Get 'tipo utilizadores' data
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipos_utilizadores_data')
        tipos_utilizadores = cursor.fetchall()

    if request.method == 'POST':
        # Get form data
        nome = request.POST['nome']
        morada = request.POST['morada']
        email = request.POST['email']
        telemovel = request.POST['telemovel']
        nif = request.POST['nif']
        estado = request.POST['estado']
        tipo_utilizador_id = request.POST['tipo_utilizador_id']

        # Call procedure to update 'utilizador'
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_utilizador(
                %s::integer, %s::varchar, %s::varchar, %s::varchar,
                %s::integer, %s::boolean, %s::integer
            )"""
            ,[id, nome, morada, email, telemovel, nif, estado, tipo_utilizador_id])

        return redirect('listar_utilizadores')

    return render(request, 'admin/editar_utilizador.html', {'utilizador': utilizador, 'tipos_utilizadores': tipos_utilizadores})

def apagar_utilizador(request, id):
    utilizador = Utilizador.objects.get(id=id)
    if request.method == 'POST':
        utilizador.delete()
        messages.success(request, f'Utilizador {utilizador.nome} foi excluido com sucesso!')
    return redirect('listar_utilizadores')



# def view_insert_user(request):
#     # Get the database connection
#     with connections['postgres'].cursor() as cursor:
#         # Call the PostgreSQL function
#         cursor.callproc('insert_into_utilizador', [
#             'morada_utilizador', 'nome', 'email', 'telemovel', None, None, None, None,'password',  # Pass your function arguments here
#         ])
        
#         # If your function returns something, fetch the result
#         result = cursor.fetchall()
        
#     # Process the result or perform further actions
#     # ...

#     # Return an HTTP response or render a template
#     print(result)
#     return render(request, 'auth/register.html')


def trocarEstado(request, id):
    with connections['postgres'].cursor() as cursor:
                cursor.execute("CALL trocar_estado_utilizador(%s)",
                               [id
                                ])
    print('!--------------------------------------------------------------------------------------------------------------------------')
    print(id)
    print('!--------------------------------------------------------------------------------------------------------------------------')
    return redirect('listar_utilizadores')

##########Fornecedores
def listar_fornecedores(request):
    with connections['postgres'].cursor() as cursor:       
        cursor.callproc('get_fornecedores_data')
        fornecedores = cursor.fetchall()
    context = {'fornecedores': fornecedores}
    print('--------------------------------------------------------------------------------------------------------------------------')
    print(fornecedores)
    print('--------------------------------------------------------------------------------------------------------------------------')
    return render(request, 'admin/listar_fornecedores.html', context)



def editar_fornecedores(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_fornecedor_by_id', [
            id
        ])
        forn = cursor.fetchone()
    print('--------------------------------------------------------------------------------------------------------------------------')
    print(forn)
    print('--------------------------------------------------------------------------------------------------------------------------')
    #TODO: Meter isto a editar, nao esta a enviar os dados para a base de dados
    print(forn)
    form = FornecedorForm(request.POST, initial={
            'nome_fornecedor': forn[1],
            'morada_fornecedor': forn[2],
            'email_fornecedor': forn[4],
            'nif': forn[3],
            'telemovel_fornecedor': forn[5],
        })
    if request.method == 'POST':
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(form.errors)
        print('--------------------------------------------------------------------------------------------------------------------------')
        if form.is_valid():
            with connections['postgres'].cursor() as cursor:
                print("Executing SQL:", cursor.mogrify("CALL update_fornecedor(%s, %s, %s, %s, %s, %s)",
                                       [id, form.cleaned_data['nome_fornecedor'],
                                        form.cleaned_data['morada_fornecedor'],
                                        form.cleaned_data['nif'],
                                        form.cleaned_data['email_fornecedor'],
                                        form.cleaned_data['telemovel_fornecedor']
                                       ]))
                cursor.execute("CALL public.update_fornecedor(%s::integer, %s::text, %s::text, %s::integer, %s::text, %s::integer)",
               [id,
                form.cleaned_data['nome_fornecedor'],
                form.cleaned_data['morada_fornecedor'],
                form.cleaned_data['nif'],
                form.cleaned_data['email_fornecedor'],
                form.cleaned_data['telemovel_fornecedor']
               ])
            return redirect('listar_fornecedores')    
    return render(request, 'admin/editar_fornecedor.html', {'forn': forn})

def apagar_fornecedores(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
                    cursor.execute("CALL delete_fornecedor_by_id(%s)",
                                [id
                                    ])
    return redirect('listar_fornecedores')

def inserir_forn(request):
    form = FornecedorForm(request.POST or None)
    print(form.errors)
    if request.method == 'POST':
        if form.is_valid():
            with connections['postgres'].cursor() as cursor:
                cursor.execute("CALL insert_fornecedor(%s, %s, %s, %s, %s)",
                            [form.cleaned_data['nome_fornecedor'],
                                form.cleaned_data['morada_fornecedor'],
                                form.cleaned_data['nif'],
                                form.cleaned_data['email_fornecedor'],
                                form.cleaned_data['telemovel_fornecedor']
                            ])
        return redirect('listar_fornecedores')
    return render(request, 'admin/inserir_forn.html', {'form': form})


#Componentes

def get_componentes(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_componentes_data')
        componentes = cursor.fetchall()
    

    return render(request, 'admin/listar_componentes.html', {'componentes': componentes})


def insert_componente(request):
    #form = ComponenteForm(request.POST or None)
    #print(form.errors)
    if request.method == 'POST':
        context = {}
        # Get form data
        print("forn_id: ",request.POST['fornecedor_id'])
        nome_componente = request.POST['nome_componente']
        stock = request.POST['stock']
        preco_compra = request.POST['preco_compra']
        peso = request.POST['peso']
        caracteristicas = request.POST['caracteristicas']
        margem_lucro = request.POST['margem_lucro']
        stock_min = request.POST['stock_min']
        fornecedor_id = request.POST['fornecedor_id']
        tipo_componente_id = request.POST['tipo_componente_id']

        # Call procedure to insert into components
        with connections['postgres'].cursor() as cursor:
            print("Executing SQL:", cursor.mogrify("CALL insert_into_componentes(%s::varchar, %s::integer, %s::float8, %s::float8, %s::varchar, %s::float8, %s::integer, %s::integer, %s::integer)",
                [
                    nome_componente, stock, preco_compra, peso,
                    caracteristicas, margem_lucro, stock_min,
                    fornecedor_id, tipo_componente_id
                ]
            ))
            cursor.execute(
                "CALL insert_into_componentes(%s::varchar, %s::integer, %s::float8, %s::float8, %s::varchar, %s::float8, %s::integer, %s::integer, %s::integer)",
                [
                    nome_componente, stock, preco_compra, peso,
                    caracteristicas, margem_lucro, stock_min,
                    fornecedor_id, tipo_componente_id
                ]
            )

        return redirect('listar_componentes')
    with connections['postgres'].cursor() as cursor:       
        cursor.callproc('get_fornecedores_data')
        fornecedores = cursor.fetchall()
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(fornecedores)
        print('--------------------------------------------------------------------------------------------------------------------------')
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_componentes_data')
        tipo_componentes = cursor.fetchall()

    return render(request, 'admin/insert_componente.html',{'fornecedores': fornecedores, 'tipo_componentes': tipo_componentes})


def update_componente(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_componente_by_id', [id])
        componente = cursor.fetchone()
    with connections['postgres'].cursor() as cursor:       
        cursor.callproc('get_fornecedores_data')
        fornecedores = cursor.fetchall()
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(fornecedores)
        print('--------------------------------------------------------------------------------------------------------------------------')
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_componentes_data')
        tipo_componentes = cursor.fetchall()
    if request.method == 'POST':
        # Get form data
        nome_componente = request.POST['nome_componente']
        stock = request.POST['stock']
        preco_compra = request.POST['preco_compra']
        peso = request.POST['peso']
        caracteristicas = request.POST['caracteristicas']
        margem_lucro = request.POST['margem_lucro']
        stock_min = request.POST['stock_min']
        fornecedor_id = request.POST['fornecedor_id']
        tipo_componente_id = request.POST['tipo_componente_id']

        # Call procedure to update component
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_componente(
                %s::integer, %s::varchar, %s::integer, %s::float8, %s::float8,
                %s::varchar, %s::float8, %s::integer, %s::integer, %s::integer
            )"""
                ,[ id, nome_componente, stock, preco_compra, peso,
                caracteristicas, margem_lucro, stock_min,
                fornecedor_id, tipo_componente_id])
        return redirect('listar_componentes')
    return render(request, 'admin/editar_componente.html', {'componente': componente,'fornecedores': fornecedores, 'tipo_componentes': tipo_componentes})

def apagar_componente(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_componente(%s)",
                           [id])
    return redirect('listar_componentes')


#--------------------------------------------------
#TipoComponente
#TODO: Acabar

def get_tipo_componentes(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_componentes_data')
        tipo_componentes = cursor.fetchall()

    return render(request, 'admin/listar_tipo_componente.html', {'tipo_componentes': tipo_componentes})


def update_tipo_componente(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_componente_by_id', [id])
        tipo_componente = cursor.fetchone()

    if request.method == 'POST':
        designacao_tipo_componente = request.POST['designacao_tipo_componente']

        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL update_tipo_componente(%s::integer,%s::text)", [id, designacao_tipo_componente])

        return redirect('listar_tipo_componentes')

    return render(request, 'admin/editar_tipo_componente.html', {'tipo_componente': tipo_componente})



def insert_into_tipo_componentes(request):
    if request.method == 'POST':
        designacao_tipo_componente = request.POST['designacao_tipo_componente']
        
        with connections['postgres'].cursor() as cursor:
            # cursor.callproc('insert_into_tipo_componentes', [designacao_tipo_componente])
            cursor.execute("CALL insert_into_tipo_componentes(%s::text)", [designacao_tipo_componente])

        return redirect('listar_tipo_componentes')

    return render(request, 'admin/insert_tipo_componente.html')

def apagar_tipo_componente(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_tipo_componente(%s)", [id])

    return redirect('listar_tipo_componentes')


#Equipamentos
def get_equipamentos(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamentos_data')
        equipamentos = cursor.fetchall()
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(equipamentos)
        print('--------------------------------------------------------------------------------------------------------------------------')

    return render(request, 'admin/listar_equipamentos.html', {'equipamentos': equipamentos})

def insert_equipamento(request):
    if request.method == 'POST':
        # Get form data
        nome_equipamento = request.POST['nome_equipamento']
        preco_equipamento = float(request.POST['preco_equipamento'])
        preco_de_producao = float(request.POST['preco_de_producao'])
        stock_equip = int(request.POST['stock_equip'])
        caracteristicas_equip = request.POST['caracteristicas_equip']
        margem_lucro_equip = float(request.POST['margem_lucro_equip'])
        stock_min_equip = int(request.POST['stock_min_equip'])
        tipo_equipamento_id = int(request.POST['tipo_equipamento_id'])
        imagem_equip = request.FILES['imagem_equip'] if 'imagem_equip' in request.FILES else None
        print('--------------------------------------------------------------------------------------------------------------------------')
        print('Bomdia')
        # print(settings.STATIC_ROOT)
        print(imagem_equip)
        print('--------------------------------------------------------------------------------------------------------------------------')
        image_path = None
        if imagem_equip:
            
            image_path = default_storage.save(imagem_equip.name, ContentFile(imagem_equip.read()))
        # Call procedure to insert into equipamentos
        with connections['postgres'].cursor() as cursor:
            
            cursor.execute(
    "CALL insert_into_equipamentos(%s::varchar, %s::float8, %s::float8, %s::integer, %s::varchar, %s::integer, %s::integer, %s::integer, %s::varchar)",
    [nome_equipamento, preco_equipamento, preco_de_producao, stock_equip, caracteristicas_equip, int(margem_lucro_equip), stock_min_equip, tipo_equipamento_id, image_path]
)


        return redirect('listar_equipamentos')

    # Fetch data needed for dropdowns (componentes, producoes, tipo de equipamentos)

    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_equipamentos_data')
        tipo_equipamentos = cursor.fetchall()

    return render(request, 'admin/insert_equipamento.html', {
        'tipo_equipamentos': tipo_equipamentos
    })


def update_equipamento(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamento_by_id', [id])
        equipamento = cursor.fetchone()

    if request.method == 'POST':
        # Get form data
        nome_equipamento = request.POST['nome_equipamento']
        preco_equipamento = request.POST['preco_equipamento']
        preco_de_producao = request.POST['preco_de_producao']
        stock_equip = request.POST['stock_equip']
        caracteristicas_equip = request.POST['caracteristicas_equip']
        margem_lucro_equip = request.POST['margem_lucro_equip']
        stock_min_equip = request.POST['stock_min_equip']
        
        tipo_equipamento_id = request.POST['tipo_equipamento_id']
        imagem_equip = request.FILES['imagem_equip'] if 'imagem_equip' in request.FILES else None
        image_path = None
        print('--------------------------------------------------------------------------------------------------------------------------')
        print('Bomdia crl')
        print(imagem_equip)
        print('--------------------------------------------------------------------------------------------------------------------------')
        if imagem_equip:
            image_path = default_storage.save(imagem_equip.name, ContentFile(imagem_equip.read()))
        # Call procedure to update equipamento
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_equipamento(
                 %s::integer,%s::float8, %s::float8, %s::integer, %s::varchar,
                %s::integer, %s::integer, %s::integer, %s::varchar,%s::varchar
            )""",
                [id, preco_equipamento, preco_de_producao, stock_equip, caracteristicas_equip,
                 margem_lucro_equip, stock_min_equip, tipo_equipamento_id,nome_equipamento, image_path]
            )

        return redirect('listar_equipamentos')

    # Fetch data needed for dropdowns (componentes, producoes, tipo de equipamentos)

    print('--------------------------------------------------------------------------------------------------------------------------')
    print(equipamento)
    print('--------------------------------------------------------------------------------------------------------------------------')

    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_equipamentos_data')
        tipo_equipamentos = cursor.fetchall()

    return render(request, 'admin/editar_equipamento.html', {
        'equipamento': equipamento,
        'tipo_equipamentos': tipo_equipamentos
    })

def apagar_equipamento(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_equipamento(%s)", [id])

    return redirect('listar_equipamentos')

# Producao

def get_producoes(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_producoes_data')
        producoes = cursor.fetchall()
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(producoes)
        print('--------------------------------------------------------------------------------------------------------------------------')

    return render(request, 'admin/listar_producao.html', {'producoes': producoes})

def insert_producao(request):
    if request.method == 'POST':
        # Get form data
        horas_producao = float(request.POST['horas_producao'])
        custos = float(request.POST['custos'])
        equipamento_id = int(request.POST['equipamento_id'])
        tipo_mao_de_obra_id = int(request.POST['tipo_mao_de_obra_id'])

        # Call procedure to insert into producao
        with connections['postgres'].cursor() as cursor:
            cursor.execute(
                "CALL insert_into_producao(%s::integer, %s::integer, %s::float8, %s::float8)",
                [ equipamento_id, tipo_mao_de_obra_id,horas_producao, custos]
            )

        return redirect('listar_producoes')

    # Fetch data needed for dropdowns (equipamentos, tipo de mao de obra)

    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamentos_data')
        equipamentos = cursor.fetchall()

        cursor.callproc('get_tipo_mao_de_obra_data')
        tipos_mao_de_obra = cursor.fetchall()

    return render(request, 'admin/insert_producao.html', {
        'equipamentos': equipamentos,
        'tipos_mao_de_obra': tipos_mao_de_obra
    })

def update_producao(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_producao_by_id', [id])
        producao = cursor.fetchone()

    if request.method == 'POST':
        # Get form data
        horas_producao = float(request.POST['horas_producao'])
        custos = float(request.POST['custos'])
        equipamento_id = int(request.POST['equipamento_id'])
        tipo_mao_de_obra_id = int(request.POST['tipo_mao_de_obra_id'])

        # Call procedure to update producao
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_producao(
                 %s::integer, %s::integer, %s::integer, %s::float8, %s::float8
            )""",
                [id, equipamento_id, tipo_mao_de_obra_id, horas_producao, custos,]
            )

        return redirect('listar_producoes')

    # Fetch data needed for dropdowns (equipamentos, tipo de mao de obra)

    print('--------------------------------------------------------------------------------------------------------------------------')
    print(producao)
    print('--------------------------------------------------------------------------------------------------------------------------')

    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamentos_data')
        equipamentos = cursor.fetchall()

        cursor.callproc('get_tipo_mao_de_obra_data')
        tipos_mao_de_obra = cursor.fetchall()

    return render(request, 'admin/editar_producao.html', {
        'producao': producao,
        'equipamentos': equipamentos,
        'tipos_mao_de_obra': tipos_mao_de_obra
    })

def apagar_producao(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_producao(%s)", [id])

    return redirect('listar_producoes')


# Tipo de Equipamentos

def get_tipo_equipamentos(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_equipamentos_data')
        tipo_equipamentos = cursor.fetchall()

    return render(request, 'admin/listar_tipo_equipamento.html', {'tipo_equipamentos': tipo_equipamentos})

def insert_tipo_equipamento(request):
    if request.method == 'POST':
        # Get form data
        designacao_tipo_equipamento = request.POST['designacao_tipo_equipamento']

        # Call procedure to insert into tipo_equipamento
        with connections['postgres'].cursor() as cursor:
            cursor.execute(
                "CALL insert_into_tipo_equipamentos(%s::varchar)",
                [designacao_tipo_equipamento]
            )

        return redirect('listar_tipo_equipamentos')

    return render(request, 'admin/insert_tipo_equipamento.html')

def update_tipo_equipamento(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_equipamentos_by_id', [id])
        tipo_equipamento = cursor.fetchone()

    if request.method == 'POST':
        # Get form data
        designacao_tipo_equipamento = request.POST['designacao_tipo_equipamento']

        # Call procedure to update tipo_equipamento
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_tipo_equipamento(
                 %s::integer,%s::varchar
            )""",
                [id, designacao_tipo_equipamento]
            )

        return redirect('listar_tipo_equipamentos')

    return render(request, 'admin/editar_tipo_equipamento.html', {'tipo_equipamento': tipo_equipamento})

def apagar_tipo_equipamento(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_tipo_equipamento(%s)", [id])

    return redirect('listar_tipo_equipamentos')

# Tipo de mao de obra

def get_tipo_mao_de_obra(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_mao_de_obra_data')
        tipo_mao_de_obra = cursor.fetchall()

    return render(request, 'admin/listar_tipo_mao_de_obra.html', {'tipo_mao_de_obra': tipo_mao_de_obra})

def inserir_tipo_mao_de_obra(request):
    if request.method == 'POST':
        descricao_tipo_mao_de_obra = request.POST['descricao_tipo_mao_de_obra']

        with connections['postgres'].cursor() as cursor:
            cursor.execute(
                "CALL insert_into_tipo_mao_de_obra(%s::varchar)",
                [descricao_tipo_mao_de_obra]
            )

        return redirect('listar_tipo_mao_de_obra')

    return render(request, 'admin/insert_tipo_mao_de_obra.html')

def update_tipo_mao_de_obra(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_mao_de_obra_by_id', [id])
        tipo_mao_de_obra = cursor.fetchone()

    if request.method == 'POST':
        # Obter dados do formulário
        descricao_tipo_mao_de_obra = request.POST['descricao_tipo_mao_de_obra']

        # Chamar procedimento para atualizar tipo_mao_de_obra
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_tipo_mao_de_obra(
                 %s::integer, %s::varchar
            )""",
                [id, descricao_tipo_mao_de_obra]
            )

        return redirect('listar_tipo_mao_de_obra')

    return render(request, 'admin/editar_tipo_mao_de_obra.html', {'tipo_mao_de_obra': tipo_mao_de_obra})

def apagar_tipo_mao_de_obra(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_tipo_mao_de_obra(%s)", [id])

    return redirect('listar_tipo_mao_de_obra')


#Carrinho

def carrinho(request):
    # Assume user authentication is implemented
    total = 0

    # Assuming the loginToken contains user and cart information
    token_string = request.COOKIES.get('loginToken')

    # Remove leading and trailing square brackets
    cleaned_string = token_string.strip('[()]')

    # Split the string using the comma as a delimiter
    values = cleaned_string.split(',')

    # Convert the string value to an integer
    v_utilizador_id = int(values[0])

    # Retrieve equipamento IDs from the Carrinho
    carrinho_items = Carrinho.objects.filter(utilizador_id=v_utilizador_id)
    equipamento_ids = [item.equipamento_id for item in carrinho_items]

    # Assuming you update the quantity in the MongoDB here

    # Call the PostgreSQL function to get equipamentos
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamentos_by_ids', [equipamento_ids])
        equipamentos = cursor.fetchall()

    # Fetch Carrinho items after updating the quantity
    carrinho_items = Carrinho.objects.filter(utilizador_id=v_utilizador_id)

    # Calculate the total price
    for equipamento in equipamentos:
        carrinho_item = next((item for item in carrinho_items if item.equipamento_id == equipamento[0]), None)
        if carrinho_item:
            total += carrinho_item.quantidade * equipamento[1]

    return render(request, 'cliente/carrinho.html', {'items': zip(equipamentos, carrinho_items), 'total': total})


def adicionar_ao_carrinho(request, p_equipamento_id):
    token_string = request.COOKIES.get('loginToken')

    # Remove leading and trailing square brackets
    cleaned_string = token_string.strip('[()]')

    # Split the string using the comma as a delimiter
    values = cleaned_string.split(',')

    # Convert the string value to an integer
    v_utilizador_id = int(values[0])

    # Check if the item is already in the cart, update the quantity if so
    item, created = Carrinho.objects.get_or_create(utilizador_id=v_utilizador_id, equipamento_id=p_equipamento_id)
    
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamento_by_id', [p_equipamento_id])
        equipamento = cursor.fetchone()

    # Check if adding the new quantity exceeds the available stock
    

    # If the item is already in the cart, update the quantity
    if created:
        item.quantidade = 1
    else:
        item.refresh_from_db()
        if item.quantidade+1 > equipamento[2]:
            with connections['postgres'].cursor() as cursor:
                cursor.callproc('get_equipamentos_data_users')
                equipamentos = cursor.fetchall()
            return render(request, 'cliente/mainmenu.html', {'equipamentos':equipamentos,'message': 'Quantidade indisponível!'})
        item.quantidade += 1
    
    item.save()

    return redirect('index')

def remover_do_carrinho(request, p_equipamento_id):
    token_string = request.COOKIES.get('loginToken')

    # Remove leading and trailing square brackets
    cleaned_string = token_string.strip('[()]')

    # Split the string using the comma as a delimiter
    values = cleaned_string.split(',')

    # Convert the string value to an integer
    v_utilizador_id = int(values[0])

    # Retrieve the cart item
    carrinho_item = get_object_or_404(Carrinho, utilizador_id=v_utilizador_id, equipamento_id=p_equipamento_id)

    # Check if the quantity is more than 1, decrease it; otherwise, remove the item
    if carrinho_item.quantidade > 1:
        carrinho_item.quantidade -= 1
        carrinho_item.save()
    else:
        carrinho_item.delete()

    return redirect('carrinho')

def limpar_carrinho(request):
    token_string = request.COOKIES.get('loginToken')

    # Remove leading and trailing square brackets
    cleaned_string = token_string.strip('[()]')

    # Split the string using the comma as a delimiter
    values = cleaned_string.split(',')

    # Convert the string value to an integer
    v_utilizador_id = int(values[0])

    # Remove all items from the cart
    Carrinho.objects.filter(utilizador_id=v_utilizador_id).delete()

    return redirect('carrinho')



def create_encomenda(request):
    # Assuming you have the user ID in the session or request
    if request.method == 'POST':
        token_string = request.COOKIES.get('loginToken')

    # Remove leading and trailing square brackets
        cleaned_string = token_string.strip('[()]')

    # Split the string using the comma as a delimiter
        values = cleaned_string.split(',')

    # Convert the string value to an integer
        utilizador_id = int(values[0])
        
        with connections['postgres'].cursor() as cursor:
            cursor.callproc('get_user_by_id', [utilizador_id])
            utilizador = cursor.fetchone()
            # Retrieve items from the Carrinho for the user
            carrinho_items = Carrinho.objects.filter(utilizador_id=utilizador_id)
            #TODO: buscar equipamento by id, fazer HTML de finalizar compra
            for carrinho_item in carrinho_items:
                    cursor.callproc('get_equipamento_by_id', [carrinho_item.equipamento_id])
                    equipamento = cursor.fetchone()
                    cursor.execute("""
                        CALL insert_into_encomendacliente(
                            %s::double precision, %s::character varying, %s::character varying,
                            %s::integer, %s::character varying, %s::character varying,
                            %s::character varying, %s::character varying, %s::integer, %s::integer
                        )
                    """, [
                        equipamento[1],#Preco equip
                        'Armazém XPTO',#morada armazem
                        request.POST['morada_encomenda'],#morada cliente
                        carrinho_item.quantidade,#qt item no carrinho
                        equipamento[8],#name artigo
                        utilizador[4],#phone cliente
                        request.POST['metodo_pagamento'],#meter na página
                        'Processamento',
                        utilizador_id,
                        carrinho_item.equipamento_id
                    ])
            # Clear the user's Carrinho after creating Encomendas
        carrinho_items.delete()
        return render(request, 'cliente/success_template.html', {'message': 'Encomenda criada com sucesso!'})
    return render(request,'cliente/finalizar_compra.html')
    

# tipo de utilizadores

def get_tipo_utilizador(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipos_utilizadores_data')
        tipos_utilizador = cursor.fetchall()
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(tipos_utilizador)
        print('--------------------------------------------------------------------------------------------------------------------------')

    return render(request, 'admin/listar_tipo_utilizador.html', {'tipos_utilizador': tipos_utilizador})

def inserir_tipo_utilizador(request):
    if request.method == 'POST':
        tipo_utilizador = request.POST['tipo_utilizador']

        with connections['postgres'].cursor() as cursor:
            cursor.execute(
                "CALL insert_into_tipo_utilizador(%s::varchar)",
                [tipo_utilizador]
            )

        return redirect('listar_tipo_utilizador')

    return render(request, 'admin/insert_tipo_utilizador.html')

def update_tipo_utilizador(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_utilizador_by_id', [id])
        tipo_utilizador = cursor.fetchone()

    if request.method == 'POST':
        # Obter dados do formulário
        tipo_utilizador = request.POST['descricao_tipo_utilizador']

        # Chamar procedimento para atualizar tipo_utilizador
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_tipo_utilizador(
                 %s::integer, %s::varchar
            )""",
                [id, tipo_utilizador]
            )

        return redirect('listar_tipo_utilizador')

    return render(request, 'admin/editar_tipo_utilizador.html', {'tipo_utilizador': tipo_utilizador})

def apagar_tipo_utilizador(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_tipo_utilizador(%s)", [id])

    return redirect('listar_tipo_utilizador')

# Funcionarios

from django.shortcuts import render, redirect
from django.db import connections
from django.http import HttpResponseForbidden

def get_funcionario(request):
    try:
        with connections['postgres'].cursor() as cursor:
            cursor.callproc('get_funcionarios_data')
            funcionarios = cursor.fetchall()
    except Exception as e:
        return HttpResponseForbidden("Você não tem permissão para acessar esses dados.")

    return render(request, 'admin/listar_funcionario.html', {'funcionarios': funcionarios})

def insert_funcionario(request):
    if request.method == 'POST':
        # Obter dados do formulário
        nome_funcionario = request.POST['nome_funcionario']
        morada_funcionario = request.POST['morada_funcionario']
        telemovel_funcionario = int(request.POST['telemovel_funcionario'])
        idade = int(request.POST['idade'])
        tipo_mao_de_obra_id = int(request.POST['tipo_mao_de_obra_id'])

        # Chamar procedimento para inserir funcionário
        with connections['postgres'].cursor() as cursor:
            cursor.execute(
                "CALL insert_into_funcionarios(%s::varchar, %s::varchar, %s::integer, %s::integer, %s::integer)",
                [nome_funcionario, morada_funcionario, telemovel_funcionario, idade, tipo_mao_de_obra_id]
            )

        return redirect('listar_funcionario')

    # Obter dados necessários para dropdowns (tipos de mão de obra)

    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_mao_de_obra_data')
        tipos_mao_de_obra = cursor.fetchall()

    return render(request, 'admin/insert_funcionario.html', {'tipos_mao_de_obra': tipos_mao_de_obra})

def editar_funcionario(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_funcionario_by_id', [id])
        funcionario = cursor.fetchone()

    if request.method == 'POST':
        # Obter dados do formulário
        nome_funcionario = request.POST['nome_funcionario']
        morada_funcionario = request.POST['morada_funcionario']
        telemovel_funcionario = int(request.POST['telemovel_funcionario'])
        idade = int(request.POST['idade'])
        tipo_mao_de_obra_id = int(request.POST['tipo_mao_de_obra_id'])

        # Chamar procedimento para atualizar funcionário
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_funcionario(
                 %s::integer, %s::varchar, %s::varchar, %s::integer, %s::integer, %s::integer
            )""",
                [id, nome_funcionario, morada_funcionario, telemovel_funcionario, idade, tipo_mao_de_obra_id]
            )

        return redirect('listar_funcionario')

    # Obter dados necessários para dropdowns (tipos de mão de obra)

    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipo_mao_de_obra_data')
        tipos_mao_de_obra = cursor.fetchall()

    return render(request, 'admin/editar_funcionario.html', {
        'funcionario': funcionario,
        'tipos_mao_de_obra': tipos_mao_de_obra
    })

def apagar_funcionario(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_funcionario(%s)", [id])

    return redirect('listar_funcionario')

# Guia de remessa

def get_guias(request):
    try:
        with connections['postgres'].cursor() as cursor:
            cursor.callproc('get_guias_de_remessa_data')
            guias = cursor.fetchall()
    except Exception as e:
        return HttpResponseForbidden("Você não tem permissão para acessar esses dados.")

    return render(request, 'admin/listar_guias_de_remessa.html', {'guias': guias})

def apagar_guia(request, id):
    if request.method == 'POST':
        with connections['postgres'].cursor() as cursor:
            cursor.execute("CALL delete_guia_de_remessa(%s)", [id])

    return redirect('listar_guia_de_remessa')