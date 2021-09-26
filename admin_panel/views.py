from django.http.response import JsonResponse
from admin_panel.forms import BrandForm
from brand.models import Brand
from product.models import Product
from account.models import Account
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth

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
    return render(request, 'admin_home.html')


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



def ad_product_list(request):
    products = Product.objects.all()
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
        slug = product_name.lower()

        product = Product(product_name=product_name, brand=brand, description=description,
                          price=price, stock=stock, image1=image1, image2=image2 ,image3=image3,image4=image4, is_available=True, slug=slug)
        product.save()
        return redirect('ad_add_product')

    brands = Brand.objects.all()
    return render(request, 'ad_add_product.html', {'brands': brands})

def ad_delete_product(request):
    id=request.POST['id']
    Product.objects.filter(id=id).delete()
    return JsonResponse({'success':True})


def active_users(request):
    users = Account.objects.order_by('id').all()
    return render(request, 'active_users.html', {'users': users})


