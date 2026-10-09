
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('style-quiz/', views.style_quiz, name='style_quiz'),
]

