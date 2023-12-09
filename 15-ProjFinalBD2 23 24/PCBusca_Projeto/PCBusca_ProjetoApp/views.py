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
from .forms import CreateUserForm,AuthForm,UtilizadorForm
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
            utilizador = form.save(commit=False)
            utilizador.nome = form.cleaned_data['nome']
            utilizador.email = email_Form
            utilizador.password = make_password(form.cleaned_data['password'])
            utilizador.NIF = form.cleaned_data['NIF'] 
            utilizador.telemovel = form.cleaned_data['telemovel'] 
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
                    form.cleaned_data['morada_utilizador'], form.cleaned_data['nome'], email_Form, form.cleaned_data['telemovel'] , None, None, None, None,make_password(form.cleaned_data['password'],'Bd2'),  # Pass your function arguments here
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

def editar_utilizador(request, id):
    utilizador = Utilizador.objects.get(id=id)
    form = UtilizadorForm(request.POST or None, instance=utilizador)
    if form.is_valid():
        form.save()
        return redirect('listar_utilizadores')
    return render(request, 'admin/editar_utilizador.html', {'form': form, 'utilizador': utilizador})

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



