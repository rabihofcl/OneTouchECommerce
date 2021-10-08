from django.http.response import JsonResponse
from admin_panel.forms import BrandForm
from brand.models import Brand
from orders.forms import OrderForm
from product.models import Product
from account.models import Account
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
import os
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderProduct 
from django.db.models import Q

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


@login_required(login_url = 'admin_signin')
def ad_logout(request):
    auth.logout(request)
    return redirect('admin_signin')


@login_required(login_url = 'admin_signin')
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


@login_required(login_url = 'admin_signin')
def ad_brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'ad_brand_list.html', {'brands': brands})



@login_required(login_url = 'admin_signin')
def ad_add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ad_brand_list')
        else:
            return redirect('ad_add_brand')
    else:
        form = BrandForm()
        return render(request, 'ad_add_brand.html', {'form': form})



@login_required(login_url = 'admin_signin')
def ad_delete_brand(request):
    id = request.POST['id']
    Brand.objects.filter(id=id).delete()
    return JsonResponse({'success': True})



@login_required(login_url = 'admin_signin')
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



@login_required(login_url = 'admin_signin')
def ad_product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'ad_product_list.html', {'products': products})



@login_required(login_url = 'admin_signin')
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



@login_required(login_url = 'admin_signin')
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



@login_required(login_url = 'admin_signin')
def ad_delete_product(request):
    id = request.POST['id']
    Product.objects.filter(id=id).delete()
    return JsonResponse({'success': True})



@login_required(login_url = 'admin_signin')
def active_users(request):
    users = Account.objects.order_by('id').filter(is_active=True).all()
    return render(request, 'active_users.html', {'users': users})



@login_required(login_url = 'admin_signin')
def blocked_users(request):
    users = Account.objects.order_by('id').filter(is_active=False).all()
    return render(request, 'blocked_users.html', {'users': users})




def ad_active_orders(request):
    active_orders = Order.objects.exclude(status='Completed').order_by('-id')
    context = {
        'active_orders': active_orders,
    }
    return render(request, 'ad_active_orders.html', context)




def ad_past_orders(request):
    past_orders = Order.objects.filter(Q(status='Completed') | Q(status='Cancelled')).order_by('-id')
    context = {
        'past_orders': past_orders,
    }
    return render(request, 'ad_past_orders.html', context)



def ad_order_edit(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)


    context = {
        'order': order,
    }
    
    return render(request, 'ad_order_edit.html', context)
