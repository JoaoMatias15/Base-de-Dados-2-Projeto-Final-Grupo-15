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

from django import forms

from .filters import EquipamentoFilter
from .forms import CreateUserForm,AuthForm,UtilizadorForm,UtilizadorForm2,FornecedorForm,ComponenteForm
from .models import Utilizador
from .models import Equipamento

# from .models import Produtos
# from .filters import ProdutosFilter
# from .forms import UtilizadorForm
# from .forms import ProdutosForm
# from .models import Fornecedores
# from .forms import FornecedoresForm
from django.db import connections

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
    equipamentos = Equipamento.objects.filter()
    print('--------------------------------------------------------------------------------------------------------------------------')
    print(equipamentos)
    print('--------------------------------------------------------------------------------------------------------------------------')
    myFilter = EquipamentoFilter(request.GET, queryset=equipamentos)
    products = myFilter.qs
    return render(request, 'cliente/mainmenu.html', {'equipamento': equipamentos, 'myFilter': myFilter})

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

def criar_utilizador(request):
    form = UtilizadorForm(request.POST or None)
    print(form.errors)
    if form.is_valid():
        form.save()
        return redirect('listar_utilizadores')
    return render(request, 'admin/criar_utilizador.html', {'form': form})

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

def editar_utilizador(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_user_by_id', [
            id
        ])
        user = cursor.fetchone()
    #TODO: Meter isto a editar, nao esta a enviar os dados para a base de dados
    print(user)
    form = UtilizadorForm2(request.POST, initial={
            'nome': user[2],
            'morada_utilizador': user[1],
            'email': user[3],
            'NIF': user[5],
            'telemovel': user[4],
        })
    if request.method == 'POST':
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(form.errors)
        print('--------------------------------------------------------------------------------------------------------------------------')
        if form.is_valid():
            print('--------------------------------------------------------------------------------------------------------------------------')
            print('ola')
            print('--------------------------------------------------------------------------------------------------------------------------')
            with connections['postgres'].cursor() as cursor:
                cursor.execute("CALL update_user(%s, %s, %s, %s, %s, %s)",
                               [id, form.cleaned_data['morada_utilizador'],
                                form.cleaned_data['nome'],
                                form.cleaned_data['email'],
                                form.cleaned_data['telemovel'],
                                form.cleaned_data['NIF']
                                ])
                print('--------------------------------------------------------------------------------------------------------------------------')
                print('adeus')
                print('--------------------------------------------------------------------------------------------------------------------------')
            return redirect('listar_utilizadores')    
    return render(request, 'admin/editar_utilizador.html', {'user': user})

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

    return render(request, 'your_template_name.html', {'tipo_componentes': tipo_componentes})


def update_tipo_componente(request, id):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_tipocomponente_by_id', [id])
        tipo_componente = cursor.fetchone()

    if request.method == 'POST':
        designacao_tipo_componente = request.POST['designacao_tipo_componente']

        with connections['postgres'].cursor() as cursor:
            cursor.callproc('update_tipo_componente', [id, designacao_tipo_componente])

        return redirect('your_redirect_url')

    return render(request, 'your_template_name.html', {'tipo_componente': tipo_componente})



def insert_into_tipo_componentes(request):
    if request.method == 'POST':
        designacao_tipo_componente = request.POST['designacao_tipo_componente']
        
        with connections['postgres'].cursor() as cursor:
            cursor.callproc('insert_into_tipo_componentes', [designacao_tipo_componente])

        return redirect('your_redirect_url')

    return render(request, 'your_template_name.html')


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

        # Call procedure to insert into equipamentos
        with connections['postgres'].cursor() as cursor:
            #query = "CALL insert_into_equipamentos(%s::varchar, %s::float8, %s::float8, %s::integer, %s::varchar, %s::float8, %s::integer, %s::integer, %s::integer)"
            #print("Executing SQL:", cursor.mogrify(query, [nome_equipamento, preco_equipamento, preco_de_producao, stock_equip, caracteristicas_equip, margem_lucro_equip, stock_min_equip, componente_id, tipo_equipamento_id]))

#             cursor.execute(
#     "CALL insert_into_equipamentos(%s::varchar, %s::float8, %s::float8, %s::integer, %s::varchar, %s::float8, %s::integer, %s::integer, %s::integer)",
#     [nome_equipamento, preco_equipamento, preco_de_producao, stock_equip, caracteristicas_equip, margem_lucro_equip, stock_min_equip, componente_id, tipo_equipamento_id]
# )      
            cursor.execute(
    "CALL insert_into_equipamentos(%s::varchar, %s::float8, %s::float8, %s::integer, %s::varchar, %s::integer, %s::integer, %s::integer)",
    [nome_equipamento, preco_equipamento, preco_de_producao, stock_equip, caracteristicas_equip, int(margem_lucro_equip), stock_min_equip, tipo_equipamento_id]
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

        # Call procedure to update equipamento
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
            CALL update_equipamento(
                 %s::integer,%s::float8, %s::float8, %s::integer, %s::varchar,
                %s::integer, %s::integer, %s::integer, %s::varchar
            )""",
                [id, preco_equipamento, preco_de_producao, stock_equip, caracteristicas_equip,
                 margem_lucro_equip, stock_min_equip, tipo_equipamento_id,nome_equipamento]
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



def get_producoes(request):
    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_producao_data')
        producoes = cursor.fetchall()
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(producoes)
        print('--------------------------------------------------------------------------------------------------------------------------')

    return render(request, 'admin/listar_producoes.html', {'producoes': producoes})

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
                "CALL insert_into_producao(%s::float8, %s::float8, %s::integer, %s::integer)",
                [horas_producao, custos, equipamento_id, tipo_mao_de_obra_id]
            )

        return redirect('listar_producoes')

    # Fetch data needed for dropdowns (equipamentos, tipo de mao de obra)

    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamentos_data')
        equipamentos = cursor.fetchall()

        cursor.callproc('get_tipos_mao_de_obra_data')
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
                 %s::integer,%s::float8, %s::float8, %s::integer, %s::integer
            )""",
                [id, horas_producao, custos, equipamento_id, tipo_mao_de_obra_id]
            )

        return redirect('listar_producoes')

    # Fetch data needed for dropdowns (equipamentos, tipo de mao de obra)

    print('--------------------------------------------------------------------------------------------------------------------------')
    print(producao)
    print('--------------------------------------------------------------------------------------------------------------------------')

    with connections['postgres'].cursor() as cursor:
        cursor.callproc('get_equipamentos_data')
        equipamentos = cursor.fetchall()

        cursor.callproc('get_tipos_mao_de_obra_data')
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