# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
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
