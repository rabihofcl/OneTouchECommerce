from django.http.response import JsonResponse
from admin_panel.forms import BrandForm
from brand.models import Brand
from product.models import Product
from account.models import Account
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
import os

# Create your views here.


def admin_signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_superuser == True:
                auth.login(request, user)
                return redirect('admin_home')
            else:
                messages.info(request, 'Not an Admin User')
                return render(request, 'admin_signin.html')
        else:
            messages.info(request, 'No User found')
            return render(request, 'admin_signin.html')

    else:
        return render(request, 'admin_signin.html')


def admin_home(request):
    products = Product.objects.all().count()
    brands = Brand.objects.all().count()
    users = Account.objects.all().count()
    context = {
        'products':products,
        'brands':brands,
        'users':users,
    }
    return render(request, 'admin_home.html', context)


def ad_brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'ad_brand_list.html', {'brands': brands})


def ad_add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('ad_brand_list')
        else:
            print('invalid')
            return redirect('ad_add_brand')
    else:
        form = BrandForm()
        return render(request, 'ad_add_brand.html', {'form': form})


def ad_delete_brand(request):
    id = request.POST['id']
    Brand.objects.filter(id=id).delete()
    return JsonResponse({'success': True})


def ad_brand_edit(request, slug):
    brand = Brand.objects.get(slug=slug)
    if request.method == 'POST':
        form = BrandForm(request.POST,request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('ad_brand_list')

    else:
        form = BrandForm(instance=brand)
        return render(request, 'ad_brand_edit.html', {'brand':brand, 'form':form})


def ad_product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'ad_product_list.html', {'products': products})


def ad_add_product(request):
    if request.method == 'POST':

        product_name = request.POST['product_name']
        brand = Brand.objects.get(brand_name=request.POST['brand'])
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        image4 = request.FILES['image4']
        slug = product_name.lower().replace(" ","-")

        product = Product(product_name=product_name, brand=brand, description=description, price=price,
                          stock=stock, image1=image1, image2=image2, image3=image3, image4=image4, is_available=True, slug=slug)
        product.save()
        return redirect('ad_add_product')

    brands = Brand.objects.all()
    return render(request, 'ad_add_product.html', {'brands': brands})


def ad_product_edit(request, id):
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(product.image1) > 0:
                os.remove(product.image1.path)
            product.image1 = request.FILES['image1']
            if len(product.image2) > 0:
                os.remove(product.image2.path)
            product.image2 = request.FILES['image2']
            if len(product.image3) > 0:
                os.remove(product.image3.path)
            product.image3 = request.FILES['image3']
            if len(product.image4) > 0:
                os.remove(product.image4.path)
            product.image4 = request.FILES['image4']

        product_name = request.POST['product_name']
        brand = Brand.objects.get(brand_name=request.POST['brand'])
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        slug = product_name.lower().replace(" ","-")

        if Product.objects.exclude(id=id).filter(product_name=product_name).exists():
            messages.info(request, 'Product already exist')
            return redirect('ad_product_edit', id=id)
        else:
            Product.objects.filter(pk=id).update(product_name=product_name, brand=brand, description=description, price=price,
                          stock=stock,  is_available=True, slug=slug)
            return redirect('ad_product_list')

    else:
        brands = Brand.objects.all()
        context = {
            'product': product,
            'brands': brands,
        }
        return render(request, 'ad_product_edit.html', context)


def ad_delete_product(request):
    id = request.POST['id']
    Product.objects.filter(id=id).delete()
    return JsonResponse({'success': True})


def active_users(request):
    users = Account.objects.order_by('id').filter(is_active=True).all()
    return render(request, 'active_users.html', {'users': users})

def blocked_users(request):
    users = Account.objects.order_by('id').filter(is_active=False).all()
    return render(request, 'blocked_users.html', {'users': users})
