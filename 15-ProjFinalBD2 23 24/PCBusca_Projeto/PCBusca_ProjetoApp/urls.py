from django.urls import path
from . import views



urlpatterns =[
    path('',views.index,name= 'index'),
    path('register',views.registerPage,name='registerPage'),
    path('login',views.login_view,name='login'),
    # path('admin', views.bomdia_admin, name='bomdia_admin'),
    # path('cart', views.cart, name='cart'),

]