from django.http.response import HttpResponse, JsonResponse
from admin_panel.forms import BrandForm
from ads.forms import AdsForm
from brand.models import Brand
from orders.forms import OrderForm, OrderProductForm
from product.forms import ProductForm
from product.models import Product
from account.models import Account
from ads.models import Ads
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
            brand = form.save()
            brand.slug = brand.brand_name.lower().replace(" ","-")
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
    brand = Brand.objects.get(slug = slug)

    if request.method == 'POST':
        form = BrandForm(request.POST,request.FILES, instance=brand)
        if form.is_valid():
            brand = form.save()
            brand.slug = brand.brand_name.lower().replace(" ","-")
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
        product_form = ProductForm(request.POST, request.FILES)
        print(product_form)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.slug = product.product_name.lower().replace(" ","-")
            product_form.save()
            return redirect('ad_add_product')
    else:
        product_form = ProductForm()

    brands = Brand.objects.all()

    context = {
        'brands': brands,
        'product_form': product_form,
    }
    return render(request, 'ad_add_product.html', context)



@login_required(login_url = 'admin_signin')
def ad_product_edit(request, id):
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.slug = product.product_name.lower().replace(" ","-")
            product_form.save()
            return redirect('ad_product_list')

    else:
        product_form = ProductForm(instance=product)

    context = {
        'product_form': product_form,
        'product': product,
    }
    return render(request, 'ad_product_edit.html',  context)



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
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    order_detail = OrderProduct.objects.exclude(Q(status='Delivered') | Q(status='Cancelled')).order_by('-created_at')  

    order_product_form = OrderProductForm()

    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    
    context = {
        'active_orders': orders,
        'orders': orders,
        'order_detail':order_detail,
        'subtotal': subtotal,
        'order_product_form': order_product_form,
    }
    return render(request, 'ad_active_orders.html', context)



def change_status(request, id):
    if request.method == 'POST':
        order_product = OrderProduct.objects.get(id=id)
        order_product_form = OrderProductForm(request.POST,instance=order_product)

        if order_product_form.is_valid():
            order_product_form.save()
            return redirect('ad_active_orders')
    return redirect('ad_active_orders')




def ad_past_orders(request):

    order_detail = OrderProduct.objects.filter(Q(status='Delivered') | Q(status='Cancelled')).order_by('-created_at')  
    order_product_form = OrderProductForm()

    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail':order_detail,
        'order_product_form': order_product_form,
    }
    return render(request, 'ad_past_orders.html', context)



def ad_order_edit(request, order_number):
    order_detail = OrderProduct.objects.filter(order__order_number=order_number)
    order = Order.objects.get(order_number=order_number)


    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)

        if order_form.is_valid():
            order_form.save()
            return redirect('ad_active_orders')
    else:
        order_form = OrderForm(instance=order)


    context = {
        'order_form': order_form,
        'order': order,
    }
    
    return render(request, 'ad_order_edit.html', context)



def ads(request):
    pass
    # ads_list = Ads.Objects.all()

    # print(ads_list)

    # context = {
    #     'ads_list': ads_list,
    # }
    # return render(request, 'ad_ads.html', context)


def ad_add_ads(request):
    pass
    # ads_form = AdsForm()


    # context = {
    #     'ads_form': ads_form,
    # }

    # return render(request, 'ad_add_ads.html', context)