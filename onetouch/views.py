from django.core import paginator
from django.db.models.aggregates import Avg
from django.http.response import HttpResponse, JsonResponse
from ads.models import Ads
from cart.views import _cart_id
from cart.models import Cart, CartItem
from brand.models import Brand
from django.http import request
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import auth
from orders.models import Order, OrderProduct, ReviewRating
from product.models import Product
from account.models import Account, Address, UserProfile
from twilio.rest import Client
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import requests
from account.forms import AddressForm, UserForm, UserProfileForm
from django.views.decorators.cache import never_cache
from decouple import config

from twilio.base.exceptions import TwilioRestException



from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all().filter(
        is_available=True).order_by('-id')[:12]

    ads = Ads.objects.all()

    context = {
        'products': products,
        'ads': ads,
    }
    return render(request, 'home.html', context)


def signin(request):
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(email=email, password=password)

            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_user_cart_exists = CartItem.objects.filter(user=user).exists()
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        if is_user_cart_exists:
                            for item in cart_item:
                                    is_item_exists = CartItem.objects.filter(user=user,product=item.product).exists()
                                    if is_item_exists:
                                        user_item = CartItem.objects.get(user=user,product=item.product)
                                        user_item.quantity += item.quantity
                                        user_item.save()
                                        if user_item.quantity > 5:
                                            user_item.quantity = 5
                                            user_item.save()
                                    else:
                                        item.user = user
                                        item.save()
                        else:
                            for item in cart_item:
                                item.user = user
                                item.save()

                except:
                    pass

                auth.login(request, user)
                request.session['user_login'] = 'user_login'
                messages.success(request, "You logged in successfully!")

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
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
        if request.method == 'POST':
            phone_number = request.POST['phone_number']

            if Account.objects.filter(phone_number=phone_number):

                request.session['phone_number'] = phone_number

                account_sid = config('account_sid')
                auth_token = config('auth_token')
                client = Client(account_sid, auth_token)

                verification = client.verify \
                    .services('VA47f566d6a44e75409506f475d3231b04') \
                    .verifications \
                    .create(to='+91'+phone_number, channel='sms')

                return redirect('phone_login_otp')

            else:
                messages.info(request, 'Phone Number is not Registered')
                return redirect('phone_login')

        return render(request, 'signin.html')

    
@never_cache
def phone_login_otp(request):
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
        if request.method == 'POST':
            otp = request.POST['otp']

            phone_number = request.session['phone_number']

            account_sid = config('account_sid')
            auth_token = config('auth_token')
            client = Client(account_sid, auth_token)

            verification_check = client.verify \
                .services('VA47f566d6a44e75409506f475d3231b04') \
                .verification_checks \
                .create(to='+91'+phone_number, code=otp)



            if verification_check.status == 'approved':

                user = Account.objects.get(phone_number=phone_number)

                if user is not None:
                    auth.login(request, user)
                    request.session['user_login'] = 'user_login'
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
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
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
                    try:
                        account_sid = config('account_sid')
                        auth_token = config('auth_token')
                        client = Client(account_sid, auth_token)

                    
                        verification = client.verify \
                            .services('VA47f566d6a44e75409506f475d3231b04') \
                            .verifications \
                            .create(to='+91'+phone_number, channel='sms')
                        

                    except TwilioRestException:
                        messages.error(request, 'Enter a valid mobile number')
                        return render(request, 'register.html')


                    return redirect('otp_register')
            else:
                messages.info(request, 'Password is not matching' ,extra_tags='twilio')
                return redirect('register')

        return render(request, 'register.html')



@never_cache
def otp_register(request):
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
        if request.method == 'POST':
            otp = request.POST['otp']

            phone_number = request.session['phone_number']

            account_sid = config('account_sid')
            auth_token = config('auth_token')
            client = Client(account_sid, auth_token)

            verification_check = client.verify \
                .services('VA47f566d6a44e75409506f475d3231b04') \
                .verification_checks \
                .create(to='+91'+phone_number, code=otp)


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

                profile = UserProfile()
                profile.user_id = user.id
                profile.profile_picture = 'pro_pic.jpg'
                profile.save()


                auth.login(request, user)
                request.session['user_login'] = 'user_login'

                # deleting details in session
                del request.session['first_name']
                del request.session['last_name']
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



@never_cache
@login_required(login_url = 'signin')
def signout(request):
        auth.logout(request)
        messages.success(request, 'You logged out successfully!')
        return redirect('home')



def forgotPass(request):
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
        if request.method == 'POST':
            phone_number = request.POST['phone_number']

            if Account.objects.filter(phone_number=phone_number):

                request.session['phone_number'] = phone_number

                account_sid = config('account_sid')
                auth_token = config('auth_token')
                client = Client(account_sid, auth_token)

                verification = client.verify \
                    .services('VA47f566d6a44e75409506f475d3231b04') \
                    .verifications \
                    .create(to='+91'+phone_number, channel='sms')

                return redirect('forgotPassOtp')

            else:
                messages.info(request, 'Phone Number is not Registered')
                return redirect('forgotPass')

        return render(request, 'forgotPass.html')


@never_cache
def forgotPassOtp(request):
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
        if request.method == 'POST':
            otp = request.POST['otp']

            phone_number = request.session['phone_number']

            account_sid = config('account_sid')
            auth_token = config('auth_token')
            client = Client(account_sid, auth_token)

            verification_check = client.verify \
                .services('VA47f566d6a44e75409506f475d3231b04') \
                .verification_checks \
                .create(to='+91'+phone_number, code=otp)


            if verification_check.status == 'approved':
                return redirect('resetPass')
            else:
                messages.info(request, 'OTP is not matching')
                return redirect('forgotPassOtp')
        else:
            return render(request, 'forgotPassOtp.html')



@never_cache
def resetPass(request):
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
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



@never_cache
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



@never_cache
def product_detail(request, brand_slug, product_slug):
    single_product = Product.objects.get(
            brand__slug=brand_slug, slug=product_slug)

    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    try:
        single_product = Product.objects.get(
            brand__slug=brand_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except:
            orderproduct = None
    else:
        orderproduct = None



    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    all_reviews = ReviewRating.objects.filter(product=single_product.id, status=True)
    rating_count=all_reviews.count()
    rating = 0
    for review in all_reviews:
        rating += review.rating
    if rating <= 0:
        avg_rating = 0
    else:
        avg_rating = rating/rating_count

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'avg_rating':avg_rating,
        'rating_count': rating_count,
    }
    return render(request, 'product_detail.html', context)



@never_cache
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword == '':
            return redirect('store')
        else:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(slug__icontains=keyword))
            product_count = products.count()
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request, 'store.html', context)


@never_cache
@login_required(login_url = 'signin')
def dashboard(request):
    if request.session.has_key('user_login'):
        orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)

        userprofile = UserProfile.objects.get(user_id=request.user.id)

        orders_count = orders.count()

        context = {
            'orders_count': orders_count,
            'userprofile': userprofile,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('home')


@never_cache
@login_required(login_url = 'signin')
def my_orders(request):
    order_detail = OrderProduct.objects.filter(user=request.user).order_by('-created_at')  
    context = {
        'order_detail':order_detail,
    }
    return render(request, 'my_orders.html', context)


@never_cache
@login_required(login_url = 'signin')
def cancel_order(request):
    id = request.POST['id']
    cancelled_product = OrderProduct.objects.get(id=id)
    Product.objects.filter(id=cancelled_product.product.id).update(stock=cancelled_product.product.stock + cancelled_product.quantity)
    OrderProduct.objects.filter(id=id).update(status='Cancelled')
    return JsonResponse({'success': True})


@never_cache
@login_required(login_url = 'signin')
def return_item(request):
    id = request.POST['id']
    OrderProduct.objects.filter(id=id).update(status='Return')
    return JsonResponse({'success': True})


@never_cache
@login_required(login_url = 'signin')
def cancel_return(request):
    id = request.POST['id']
    OrderProduct.objects.filter(id=id).update(status='Delivered')
    return JsonResponse({'success': True})


@never_cache
@login_required(login_url = 'signin')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance = request.user)
        profile_form = UserProfileForm(instance = userprofile)
        

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'edit_profile.html', context)


@never_cache
@login_required(login_url = 'signin')
def my_addresses(request):
    address_form = AddressForm()

    addresses = Address.objects.filter(user=request.user)

    context = {
        'address_form': address_form,
        'addresses': addresses,
    }

    return render(request, 'my_addresses.html', context)



@never_cache
@login_required(login_url = 'signin')
def add_address(request):
    address_form = AddressForm(request.POST)
    if address_form.is_valid():
        address = address_form.save(commit=False)
        address.user = request.user
        address.save()
    return JsonResponse({'success': True})




@never_cache
@login_required(login_url = 'signin')
def delete_address(request):
    address_id = request.POST['id']
    Address.objects.filter(id=address_id).delete()
    return JsonResponse({'success': True})


@never_cache
@login_required(login_url = 'signin')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('change_password')
            else:
                messages.info(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.info(request, 'Password is not matching!')
            return redirect('change_password')

    return render(request, 'change_password.html')



@never_cache
@login_required(login_url = 'signin')
def order_details(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)

    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail':order_detail,
        'order': order,
        'subtotal': subtotal
    }
    return render(request, 'order_details.html', context)