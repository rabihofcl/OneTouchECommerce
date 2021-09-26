from brand.models import Brand
from django.http import request
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import auth
from product.models import Product
from account.models import Account


def home(request):
    products = Product.objects.all().filter(
        is_available=True).order_by('-id')[:12]

    context = {
        'products': products,
    }
    return render(request, 'home.html', context)


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'No User found')
            return render(request, 'signin.html')

    else:
        return render(request, 'signin.html')


def apple(request):
    products = Product.objects.all().filter(
        is_available=True, brand__brand_name='Apple')

    return render(request, 'apple.html', {'products': products, })


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if Account.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif Account.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('register')
            elif Account.objects.filter(phone_number=phone_number).exists():
                messages.info(request, 'Phone number already taken')
                return redirect('register')
            else:
                user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                                   username=username, password=password1, email=email, phone_number=phone_number)
                user.save()
                return redirect('home')
        else:
            messages.info(request, 'Password is not matching')
            return redirect('register')

    return render(request, 'register.html')


def signout(request):
    auth.logout(request)
    return redirect('home')


def store(request, brand_slug=None):
    brands = None
    products = None

    if brand_slug != None:
        brands = get_object_or_404(Brand, slug=brand_slug)
        products = Product.objects.filter(brand=brands, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all()
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)


def product_detail(request, brand_slug, product_slug):
    try:
        single_product = Product.objects.get(
            brand__slug=brand_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
    }
    return render(request, 'product_detail.html', context)
