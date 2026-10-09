
import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Product, Order


def home(request):
    products = Product.objects.all()
    return render(
        request,
        'store/home.html',
        {'products': products}
    )


def cart(request):
    return render(request, 'store/cart.html')


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(
        request,
        'store/product_detail.html',
        {'product': product}
    )


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')

        return render(
            request,
            'store/login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'store/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(
                request,
                'store/register.html',
                {'error': 'Passwords do not match.'}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'store/register.html',
                {'error': 'Username already exists.'}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/login/')

    return render(request, 'store/register.html')


def checkout(request):
    if request.method == 'POST':
        cart_data = request.POST.get('cart_data')

        if not cart_data:
            return redirect('/cart/')

        cart_items = json.loads(cart_data)

        for item in cart_items:
            Order.objects.create(
                username=(
                    request.user.username
                    if request.user.is_authenticated
                    else 'Guest'
                ),
                product_name=item['name'],
                price=item['price'],
                quantity=1
            )

        return render(request, 'store/order_success.html')

    return redirect('/cart/')


def style_quiz(request):
    products = Product.objects.all()
    return render(
        request,
        'store/style_quiz.html',
        {'products': products}
    )
