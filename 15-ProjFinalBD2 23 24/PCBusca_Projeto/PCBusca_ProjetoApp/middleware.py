# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.db import connections

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Test Middleware: TokenMiddleware')
        # Check if loginToken is present in the request
        if 'loginToken' not in request.COOKIES:
            # Exclude certain URLs from the check
            excluded_urls = [reverse('login'), reverse('index')]
            current_url = request.path

            if current_url not in excluded_urls:
                # Redirect to the login page if loginToken is missing
                return redirect(reverse('login'))  # Adjust 'login' to your actual login URL

        response = self.get_response(request)
        return response

class AdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.path.startswith('/PCBusca_ProjetoApp/admin'):
            token_string = request.COOKIES.get('loginToken')
            print('Test Middleware: AdminCheckMiddleware')
            # Remove leading and trailing square brackets
            cleaned_string = token_string.strip('[()]')

            # Split the string using the comma as a delimiter
            values = cleaned_string.split(',')

            # Convert the string value to an integer
            v_utilizador_id = int(values[0])
            with connections['postgres'].cursor() as cursor:
                cursor.callproc('get_tipo_desc_user_id', [v_utilizador_id])
                tipouser = cursor.fetchone()
            if tipouser[0] != 'Administrador':
                return redirect(reverse('index'))
        return self.get_response(request)
            