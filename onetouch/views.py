from django.core import paginator
from django.http.response import HttpResponse
from cart.views import _cart_id
from cart.models import Cart, CartItem
from brand.models import Brand
from django.http import request
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import auth
from product.models import Product
from account.models import Account
from twilio.rest import Client
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import requests



from django.contrib.auth.decorators import login_required


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
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()

            except:
                pass

            auth.login(request, user)

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')

        else:
            messages.info(request, 'No User found')
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')



def phone_login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']

        if Account.objects.filter(phone_number=phone_number):

            request.session['phone_number'] = phone_number

            account_sid = "ACbd2e01de49095381f621169be1ce4e98"
            auth_token = "44b8aceacd094dacc3cf29f80b1f30e3"
            client = Client(account_sid, auth_token)

            verification = client.verify \
                .services('VA47f566d6a44e75409506f475d3231b04') \
                .verifications \
                .create(to='+91'+phone_number, channel='sms')

            print(verification.status)
            return redirect('phone_login_otp')

        else:
            messages.info(request, 'Phone Number is not Registered')
            return redirect('phone_login')

    return render(request, 'signin.html')

    

def phone_login_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']

        phone_number = request.session['phone_number']

        account_sid = "ACbd2e01de49095381f621169be1ce4e98"
        auth_token = "44b8aceacd094dacc3cf29f80b1f30e3"
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
            .services('VA47f566d6a44e75409506f475d3231b04') \
            .verification_checks \
            .create(to='+91'+phone_number, code=otp)

        print(verification_check.status)

        if verification_check.status == 'approved':

            user = Account.objects.get(phone_number=phone_number)

            if user is not None:
                auth.login(request, user)
                del request.session['phone_number']
                return redirect('home')
            else:
                return redirect('phone_login_otp')

        else:
            messages.info(request, 'OTP is not matching')
            return redirect('phone_login_otp')
    else:
        return render(request, 'phone_login_otp.html')




def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # saving details to session

        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['username'] = username
        request.session['email'] = email
        request.session['phone_number'] = phone_number
        request.session['password'] = password1

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

                account_sid = "ACbd2e01de49095381f621169be1ce4e98"
                auth_token = "44b8aceacd094dacc3cf29f80b1f30e3"
                client = Client(account_sid, auth_token)

                verification = client.verify \
                    .services('VA47f566d6a44e75409506f475d3231b04') \
                    .verifications \
                    .create(to='+91'+phone_number, channel='sms')

                print(verification.status)

                return redirect('otp_register')
        else:
            messages.info(request, 'Password is not matching')
            return redirect('register')

    return render(request, 'register.html')




def otp_register(request):

    if request.method == 'POST':
        otp = request.POST['otp']

        phone_number = request.session['phone_number']

        account_sid = "ACbd2e01de49095381f621169be1ce4e98"
        auth_token = "44b8aceacd094dacc3cf29f80b1f30e3"
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
            .services('VA47f566d6a44e75409506f475d3231b04') \
            .verification_checks \
            .create(to='+91'+phone_number, code=otp)

        print(verification_check.status)

        if verification_check.status == 'approved':
            first_name = request.session['first_name']
            last_name = request.session['last_name']
            username = request.session['username']
            email = request.session['email']
            phone_number = request.session['phone_number']
            password = request.session['password']

            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                               username=username, email=email, phone_number=phone_number, password=password)
            user.save()
            auth.login(request, user)

            # deleting details in session

            del request.session['last_name']
            del request.session['first_name']
            del request.session['username']
            del request.session['email']
            del request.session['phone_number']
            del request.session['password']

            return redirect('home')

        else:
            messages.info(request, 'OTP is not matching')
            return redirect('otp_register')
    else:
        return render(request, 'otp_register.html')




@login_required(login_url = 'signin')
def signout(request):
    auth.logout(request)
    return redirect('home')



def forgotPass(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']

        if Account.objects.filter(phone_number=phone_number):

            request.session['phone_number'] = phone_number

            account_sid = "ACbd2e01de49095381f621169be1ce4e98"
            auth_token = "44b8aceacd094dacc3cf29f80b1f30e3"
            client = Client(account_sid, auth_token)

            verification = client.verify \
                .services('VA47f566d6a44e75409506f475d3231b04') \
                .verifications \
                .create(to='+91'+phone_number, channel='sms')

            print(verification.status)
            return redirect('forgotPassOtp')

        else:
            messages.info(request, 'Phone Number is not Registered')
            return redirect('forgotPass')

    return render(request, 'forgotPass.html')


def forgotPassOtp(request):
    if request.method == 'POST':
        otp = request.POST['otp']

        phone_number = request.session['phone_number']

        account_sid = "ACbd2e01de49095381f621169be1ce4e98"
        auth_token = "44b8aceacd094dacc3cf29f80b1f30e3"
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
            .services('VA47f566d6a44e75409506f475d3231b04') \
            .verification_checks \
            .create(to='+91'+phone_number, code=otp)

        print(verification_check.status)

        if verification_check.status == 'approved':
            return redirect('resetPass')
        else:
            messages.info(request, 'OTP is not matching')
            return redirect('forgotPassOtp')
    else:
        return render(request, 'forgotPassOtp.html')




def resetPass(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            phone_number = request.session['phone_number']
            user = Account.objects.get(phone_number=phone_number)
            user.set_password(password1)
            user.save()

            del request.session['phone_number']

            return redirect('signin')

        else:
            messages.info(request, 'Password is not matching')
            return redirect('resetPass')
    else:
        return render(request, 'resetPass.html')




def store(request, brand_slug=None):
    
    brands = None
    products = None

    if brand_slug != None:
        brands = get_object_or_404(Brand, slug=brand_slug)
        products = Product.objects.filter(brand=brands, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)


def product_detail(request, brand_slug, product_slug):
    try:
        single_product = Product.objects.get(
            brand__slug=brand_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    return render(request, 'product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(slug__icontains=keyword))
            product_count = products.count()
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request, 'store.html', context)



@login_required(login_url = 'signin')
def dashboard(request):
    return render(request, 'dashboard.html')