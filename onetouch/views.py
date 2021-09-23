from django.http import request
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from product.models import Product

def home(request):
    return render(request, 'home.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request,'No User found')
            return render(request,'signin.html')

    else:
        return render(request,'signin.html')


def apple(request):
    products = Product.objects.all().filter(is_available=True, brand__brand_name='Apple')

    context = {
        'products':products,
    }
    return render(request, 'apple.html', context)

def samsung(request):
    products = Product.objects.all().filter(is_available=True, brand__brand_name='Samsung')

    context = {
        'products':products,
    }
    return render(request, 'samsung.html', context)

def huawei(request):
    products = Product.objects.all().filter(is_available=True, brand__brand_name='Huawei')

    context = {
        'products':products,
    }
    return render(request, 'huawei.html', context)

def xiaomi(request):
    products = Product.objects.all().filter(is_available=True, brand__brand_name='Xiaomi')

    context = {
        'products':products,
    }
    return render(request, 'xiaomi.html', context)

def vivo(request):
    products = Product.objects.all().filter(is_available=True, brand__brand_name='Vivo')

    context = {
        'products':products,
    }
    return render(request, 'vivo.html', context)

def oppo(request):
    products = Product.objects.all().filter(is_available=True, brand__brand_name='Oppo')

    context = {
        'products':products,
    }
    return render(request, 'oppo.html', context)

def motorola(request):
    products = Product.objects.all().filter(is_available=True, brand__brand_name='Motorola')

    context = {
        'products':products,
    }
    return render(request, 'motorola.html', context)



def register(request):
    return render(request,'register.html')


def signout(request):
    auth.logout(request)
    return redirect('home')